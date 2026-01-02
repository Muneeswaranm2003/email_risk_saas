def evaluate_dkim_alignment(from_domain, dkim_domain, dkim_result):
    if dkim_result != "pass":
        return "fail"

    if dkim_domain == from_domain:
        return "verified_aligned"

    return "verified_unaligned"
