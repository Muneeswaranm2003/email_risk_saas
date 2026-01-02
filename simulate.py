from fastapi import APIRouter
from app.schemas.simulate_schema import SimulateRequest
from fastapi import Depends
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.database import SessionLocal
from app.models.simulation import Simulation

from app.services.domain_check import check_spf, check_dmarc
from app.services.dkim_status import get_dkim_status
from app.risk_engine.evaluator import evaluate_risk
from app.risk_engine.scorer import risk_level

router = APIRouter()

@router.post("/simulate")
def simulate(payload: SimulateRequest, current_user: User = Depends(get_current_user)):
    domain = payload.domain

    # 1️⃣ Get DKIM status (DNS + logic)
    dkim_info = get_dkim_status(domain)

    # 2️⃣ Prepare data for risk engine
    data = {
        "spf": check_spf(domain),
        "dmarc": check_dmarc(domain),
        "dkim_status": dkim_info["status"],
        "dkim_selectors": dkim_info["selectors"],
        "planned_volume": payload.planned_volume,
        "avg_volume": payload.avg_volume
    }

    # 3️⃣ Calculate risk
    score, issues = evaluate_risk(data)
    final_risk = risk_level(score)

    def serialize_issues(issues):
        clean = []

        for issue in issues:
            clean.append({
                "id": issue.get("id"),
                "weight": issue.get("weight"),
                "reason": issue.get("reason"),
                "fix": issue.get("fix")
            })

        return clean
    
    # 4️⃣ SAVE RESULT TO DATABASE  ✅
    clean_issues = serialize_issues(issues)
    db = SessionLocal()

    db_simulation = Simulation(
    user_id=current_user.id,   # 🔥 ADD THIS
    domain=domain,
    planned_volume=payload.planned_volume,
    avg_volume=payload.avg_volume,
    spf=str(data["spf"]),
    dmarc=str(data["dmarc"]),
    dkim_status=data["dkim_status"],
    dkim_selector=...,
    risk_score=score,
    risk_level=final_risk,
    issues=clean_issues
)

    db.add(db_simulation)
    db.commit()
    db.refresh(db_simulation)
    db.close()
    
    # 5️⃣ Return response to client
    return {
        "simulation_id": db_simulation.id,
        "domain": domain,
        "spf": data["spf"],
        "dmarc": data["dmarc"],
        "dkim": dkim_info,
        "score": score,
        "risk": final_risk,
        "issues": issues,
        "created_at": db_simulation.created_at
    }
    