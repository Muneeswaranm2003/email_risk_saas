import dns.resolver

resolver = dns.resolver.Resolver()
resolver.nameservers = ["8.8.8.8", "1.1.1.1"]
resolver.timeout = 5
resolver.lifetime = 5

COMMON_SELECTORS = [
    "default",
    "selector1",
    "selector2",
    "google",
    "k1",
    "k2",
    "mail",
    "smtp",
    "s1",
    "s2"
]

def discover_dkim(domain):
    found = []

    for selector in COMMON_SELECTORS:
        dkim_domain = f"{selector}._domainkey.{domain}"
        try:
            answers = resolver.resolve(dkim_domain, "TXT")
            for rdata in answers:
                record = "".join(
                    part.decode() if isinstance(part, bytes) else part
                    for part in rdata.strings
                ).lower()

                if record.startswith("v=dkim1"):
                    found.append(selector)

        except Exception:
            continue

    return found
