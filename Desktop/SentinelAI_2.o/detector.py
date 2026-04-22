import re

# Regex patterns
EMAIL_REGEX = r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+"
PHONE_REGEX = r"\b\d{10}\b"

def detect_sensitive_data(text: str):
    import spacy
    nlp = spacy.load("en_core_web_sm")   # ✅ load inside function

    doc = nlp(text)

    detected = {}

    # 🔹 NER Detection (ML-based)
    for ent in doc.ents:
        label = ent.label_

        # ✅ Small correction for misclassified names
        if label == "GPE" and ent.text.istitle():
            label = "PERSON"

        if label in ["PERSON", "ORG", "GPE"]:
            if label not in detected:
                detected[label] = []
            detected[label] = list(set(detected[label] + [ent.text]))

    # 🔹 Regex Detection (Structured Data)

    # ✅ Email fix (remove trailing punctuation)
    emails = [email.strip(".") for email in re.findall(EMAIL_REGEX, text)]
    emails = list(set(emails))
    if emails:
        detected["EMAIL"] = emails

    # ✅ Phone detection
    phones = list(set(re.findall(PHONE_REGEX, text)))
    if phones:
        detected["PHONE"] = phones

    return detected