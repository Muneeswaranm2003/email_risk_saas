from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.simulation import Simulation
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/history", tags=["History"])

@router.get("/")
def get_history(
    domain: str | None = Query(default=None),
    limit: int = Query(default=10, le=100),
    current_user: User = Depends(get_current_user)
):
    db: Session = SessionLocal()

    query = db.query(Simulation).filter(
        Simulation.user_id == current_user.id
    )

    if domain:
        query = query.filter(Simulation.domain == domain)

    simulations = (
        query
        .order_by(Simulation.created_at.desc())
        .limit(limit)
        .all()
    )

    total = query.count()

    result = [
        {
            "id": s.id,
            "domain": s.domain,
            "risk_score": s.risk_score,
            "risk_level": s.risk_level,
            "spf": s.spf,
            "dmarc": s.dmarc,
            "dkim_status": s.dkim_status,
            "created_at": s.created_at
        }
        for s in simulations
    ]

    db.close()

    return {
        "total": total,
        "items": result
    }
