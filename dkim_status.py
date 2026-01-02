from app.services.dkim_check import discover_dkim

PROVIDER_DOMAINS = [
    "gmail.com",
    "google.com",
    "outlook.com",
    "hotmail.com",
    "yahoo.com"
]

def get_dkim_status(domain):
    selectors = discover_dkim(domain)

    if selectors:
        return {
            "status": "configured",
            "selectors": selectors
        }

    if domain in PROVIDER_DOMAINS:
        return {
            "status": "not_detected",
            "selectors": []
        }

    return {
        "status": "missing",
        "selectors": []
    }
