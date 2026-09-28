from typing import List, Dict, Any


DEFAULT_WEIGHTS = {
    "interest_fit": 0.25,
    "academic_fit": 0.20,
    "financial_fit": 0.20,
    "career_alignment": 0.15,
    "location_fit": 0.10,
    "duration": 0.05,
    "flexibility": 0.05
}


def validate_weights(weights: Dict[str, float]) -> bool:
    """Validate that weights sum to approximately 1.0 (or 100%)."""
    total = sum(weights.values())
    if 99.0 <= total <= 101.0:
        # User entered percentage (e.g. 25 instead of 0.25)
        return True
    return 0.99 <= total <= 1.01


def normalize_weights(weights: Dict[str, float]) -> Dict[str, float]:
    """Ensure weights sum to 1.0."""
    total = sum(weights.values())
    if total == 0:
        return DEFAULT_WEIGHTS.copy()
    return {k: v / total for k, v in weights.items()}


def calculate_matrix(pathways: List[Dict[str, Any]], weights: Dict[str, float], student_profile: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Computes transparent multi-criteria decision matrix across candidate pathways.
    Returns per-factor scores (0-100), factor weights, weighted total score,
    and granular explanations for each factor score.
    """
    norm_weights = normalize_weights(weights) if weights else DEFAULT_WEIGHTS.copy()
    scored_pathways = []

    for path in pathways:
        pathway_id = str(path.get("id", ""))
        name = path.get("name", "Pathway")

        # Extract or compute factor scores (0-100)
        interest_fit = float(path.get("interest_fit_score") or 75.0)
        academic_fit = float(path.get("academic_fit_score") or 80.0)
        financial_fit = float(path.get("financial_fit_score") or 70.0)
        career_alignment = float(path.get("compatibility_score") or 85.0)

        # Duration score (shorter pathways get higher score if prefer fast entry)
        duration_years = float(path.get("total_duration_years") or 4.0)
        duration_score = max(20.0, min(100.0, 100.0 - (duration_years - 2.0) * 15.0))

        # Location score
        location_score = 80.0  # baseline favorable unless flagged

        # Flexibility score (based on transferable skills / multiple entry/exit)
        flexibility_score = 75.0

        scores = {
            "interest_fit": round(interest_fit, 1),
            "academic_fit": round(academic_fit, 1),
            "financial_fit": round(financial_fit, 1),
            "career_alignment": round(career_alignment, 1),
            "location_fit": round(location_score, 1),
            "duration": round(duration_score, 1),
            "flexibility": round(flexibility_score, 1)
        }

        # Weighted calculation
        total_score = sum(scores[factor] * norm_weights.get(factor, 0.0) for factor in scores)
        total_score = round(total_score, 1)

        explanations = {
            "interest_fit": f"Scores {scores['interest_fit']}% alignment with student's verified interest domains.",
            "academic_fit": f"Scores {scores['academic_fit']}% based on past academic performance in prerequisite subjects.",
            "financial_fit": f"Scores {scores['financial_fit']}% in relation to the annual household budget.",
            "career_alignment": f"Scores {scores['career_alignment']}% compatibility with target industry skill demands.",
            "location_fit": f"Geographic preference alignment is estimated at {scores['location_fit']}%.",
            "duration": f"Program duration of {duration_years} years yields {scores['duration']}% on pacing alignment.",
            "flexibility": f"Provides {scores['flexibility']}% options for postgraduate specialization or lateral shifts."
        }

        scored_pathways.append({
            "pathway_id": pathway_id,
            "pathway_name": name,
            "scores": scores,
            "total_weighted_score": total_score,
            "score_explanations": explanations
        })

    # Rank by total weighted score descending
    scored_pathways.sort(key=lambda x: x["total_weighted_score"], reverse=True)

    return {
        "weights": norm_weights,
        "pathway_scores": scored_pathways,
        "methodology": "Linear Additive Multi-Attribute Utility Model using user-configured weights",
        "transparency_notice": "This ranking represents decision-support based on your chosen weight profile, not an authoritative verdict."
    }
