import re

def parse_auth_results(message):
    """
    message: pyzmail.PyzMessage
    """

    result = {
        "dkim": "unknown",
        "dkim_selector": None,
        "dkim_domain": None,
        "spf": "unknown"
    }

    # PyzMail stores headers as a list of tuples
    headers = message._headers

    for name, value in headers:
        name = name.lower()
        value = value.lower()

        # Authentication-Results header
        if name == "authentication-results":
            if "dkim=pass" in value:
                result["dkim"] = "pass"
            elif "dkim=fail" in value:
                result["dkim"] = "fail"

            if "spf=pass" in value:
                result["spf"] = "pass"
            elif "spf=fail" in value:
                result["spf"] = "fail"

        # DKIM-Signature header
        if name == "dkim-signature":
            s = re.search(r"s=([^;]+)", value)
            d = re.search(r"d=([^;]+)", value)

            if s:
                result["dkim_selector"] = s.group(1)
            if d:
                result["dkim_domain"] = d.group(1)

    return result
