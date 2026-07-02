# explainability.py

def generate_explanation(
    semantic_score,
    role_fit,
    matched_skills
):
    """
    Generate explanation for recruiter.
    """

    explanation = []

    # Semantic Score
    if semantic_score >= 0.80:
        explanation.append("Excellent semantic similarity")
    elif semantic_score >= 0.65:
        explanation.append("High semantic similarity")
    else:
        explanation.append("Moderate semantic similarity")

    # Role Fit
    if role_fit >= 0.80:
        explanation.append("Excellent role fit")
    elif role_fit >= 0.50:
        explanation.append("Good role fit")
    elif role_fit > 0:
        explanation.append("Partial role fit")
    else:
        explanation.append("Low role fit")

    # Matched Skills
    if matched_skills:
        explanation.append(
            "Matched Skills: " +
            ", ".join(matched_skills)
        )
    else:
        explanation.append(
            "No matching skills found"
        )

    return " | ".join(explanation)