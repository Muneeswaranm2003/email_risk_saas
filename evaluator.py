from app.risk_engine.rules import RISK_RULES

def evaluate_risk(data):
    triggered = []
    total_score = 0

    for rule in RISK_RULES:
        if rule["condition"](data):
            triggered.append(rule)
            total_score += rule["weight"]

    return total_score, triggered
