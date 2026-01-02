import dns.resolver

resolver = dns.resolver.Resolver()
resolver.nameservers = ["8.8.8.8", "1.1.1.1"]
resolver.timeout = 5
resolver.lifetime = 5


def _get_txt_records(domain):
    try:
        answers = resolver.resolve(domain, "TXT")
        records = []

        for rdata in answers:
            txt = ""
            for part in rdata.strings:
                if isinstance(part, bytes):
                    txt += part.decode()
                else:
                    txt += part
            records.append(txt.lower())

        return records

    except Exception:
        return []


def check_spf(domain):          # ✅ MUST EXIST
    records = _get_txt_records(domain)
    return any(record.startswith("v=spf1") for record in records)


def check_dmarc(domain):        # ✅ MUST EXIST
    records = _get_txt_records(f"_dmarc.{domain}")
    return any(record.startswith("v=dmarc1") for record in records)
