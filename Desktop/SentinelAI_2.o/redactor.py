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


def restore_text(text: str, mapping: dict):
    for placeholder, original in mapping.items():
        text = text.replace(placeholder, original)
    return text