RISK_RULES = [
    {
        "id": "SPF_MISSING",
        "condition": lambda d: not d["spf"],
        "weight": 15,
        "reason": "SPF record is missing",
        "fix": "Add SPF record to your DNS"
    },
    {
        "id": "DMARC_MISSING",
        "condition": lambda d: not d["dmarc"],
        "weight": 15,
        "reason": "DMARC record is missing",
        "fix": "Add DMARC policy with p=none"
    },
    {
        # Only penalize when DKIM is clearly missing
        "id": "DKIM_MISSING",
        "condition": lambda d: d["dkim_status"] == "missing",
        "weight": 20,
        "reason": "DKIM is not configured for this domain",
        "fix": "Configure DKIM with your email provider"
    },
    {
        # Informational, not heavy risk
        "id": "DKIM_NOT_DETECTED",
        "condition": lambda d: d["dkim_status"] == "not_detected",
        "weight": 5,
        "reason": "DKIM not detected via DNS",
        "fix": "Send a test email to verify DKIM"
    }
]
