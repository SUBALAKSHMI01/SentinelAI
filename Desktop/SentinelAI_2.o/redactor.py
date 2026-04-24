import re

# 🔐 Redaction
def redact_text(text: str, detected: dict):
    mapping = {}
    counter = {}

    for entity_type, values in detected.items():
        counter.setdefault(entity_type, 0)

        for value in values:
            placeholder = f"[{entity_type}_{counter[entity_type]}]"

            # ✅ Safe replace
            text = re.sub(re.escape(value), placeholder, text)

            mapping[placeholder] = value
            counter[entity_type] += 1

    return text, mapping


# 🔄 Restore (ONLY FULL RESTORE now)
def restore_text(text: str, mapping: dict, role: str):
    # Only admin & employee → both full restore
    for placeholder, original in mapping.items():
        text = text.replace(placeholder, original)

    return text