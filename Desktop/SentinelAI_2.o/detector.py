import re
import spacy

# ✅ Load once
nlp = spacy.load("en_core_web_sm")

# 🔐 Strong regex patterns
PATTERNS = {
    "EMAIL": r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+",
    "PHONE": r"\b[6-9]\d{9}\b",
    "AADHAAR": r"\b\d{12}\b",
    "ACCOUNT_NUMBER": r"\b\d{9,18}\b",  # generic bank account range
    "PASSWORD": r"(password\s*[:=]\s*\S+)",
    "API_KEY": r"(api[_-]?key\s*[:=]\s*\S+)",
}

def detect_sensitive_data(text: str):
    detected = {}

    # 🔹 NER Detection (Names, Orgs)
    doc = nlp(text)
    for ent in doc.ents:
        label = ent.label_

        if label == "GPE" and ent.text.istitle():
            label = "PERSON"

        if label in ["PERSON", "ORG"]:
            detected.setdefault(label, []).append(ent.text)

    # 🔹 Regex Detection
    for key, pattern in PATTERNS.items():
        matches = re.findall(pattern, text, re.IGNORECASE)

        # Flatten tuples if any
        matches = [m if isinstance(m, str) else m[0] for m in matches]

        if matches:
            detected[key] = list(set(matches))

    return detected