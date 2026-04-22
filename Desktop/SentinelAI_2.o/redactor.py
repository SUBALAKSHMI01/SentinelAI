import re

EMAIL_REGEX = r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+"
PHONE_REGEX = r"\b\d{10}\b"

def redact_text(text: str):
    mapping = {}

    # Replace emails
    emails = re.findall(EMAIL_REGEX, text)
    for i, email in enumerate(set(emails)):
        placeholder = f"[EMAIL_{i}]"
        text = text.replace(email, placeholder)
        mapping[placeholder] = email

    # Replace phone numbers
    phones = re.findall(PHONE_REGEX, text)
    for i, phone in enumerate(set(phones)):
        placeholder = f"[PHONE_{i}]"
        text = text.replace(phone, placeholder)
        mapping[placeholder] = phone

    return text, mapping


# 🔥 NEW: Partial masking logic
def partial_mask(value: str, entity_type: str):
    if entity_type == "EMAIL":
        parts = value.split("@")
        return parts[0][0] + "***@" + parts[1]

    elif entity_type == "PHONE":
        return value[:2] + "****" + value[-2:]

    return "[MASKED]"


# 🔥 UPDATED restore (role-based)
def restore_text(text: str, mapping: dict, role: str):
    for placeholder, original in mapping.items():

        entity_type = placeholder.split("_")[0].replace("[", "")

        # ✅ Admin & Employee → FULL restore
        if role.lower() in ["admin", "employee"]:
            replacement = original

        # ✅ External → PARTIAL restore
        elif role.lower() == "external":
            replacement = partial_mask(original, entity_type)

        else:
            replacement = original  # fallback

        text = text.replace(placeholder, replacement)

    return text