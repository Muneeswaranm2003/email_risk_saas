def risk_level(score):
    if score <= 30:
        return "LOW"
    elif score <= 60:
        return "MEDIUM"
    return "HIGH"
