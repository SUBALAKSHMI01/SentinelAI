def calculate_risk(detected_data: dict):
    score = 0

    weights = {
        "PERSON": 2,
        "EMAIL": 5,
        "PHONE": 5,
        "ORG": 1,
        "GPE": 1
    }

    for entity, values in detected_data.items():
        weight = weights.get(entity, 0)
        score += weight * len(values)

    # 🔹 Risk Level Decision
    if score >= 7:
        level = "HIGH"
    elif score >= 3:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level