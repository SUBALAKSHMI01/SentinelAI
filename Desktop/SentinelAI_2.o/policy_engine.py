def apply_policy(role: str, risk_level: str):
    # Simple policy rules

    if role == "admin":
        return "ALLOW"

    if risk_level == "HIGH":
        return "STRICT_REDACT"

    if risk_level == "MEDIUM":
        return "REDACT"

    return "ALLOW"