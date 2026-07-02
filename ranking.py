# ranking.py

def calculate_final_score(semantic_score, role_fit):
    """
    Calculate final candidate score.

    Parameters:
        semantic_score (float): Similarity score from Retrieval Module
        role_fit (float): Role Fit score (0-1)

    Returns:
        float: Final score
    """

    semantic_weight = 0.70
    role_fit_weight = 0.30

    final_score = (
        semantic_weight * semantic_score
        +
        role_fit_weight * role_fit
    )

    return round(final_score, 4)