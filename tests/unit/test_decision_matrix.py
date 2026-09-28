import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../apps/api")))

from app.domains.decision_matrix.engine import (
    validate_weights,
    normalize_weights,
    calculate_matrix,
    DEFAULT_WEIGHTS
)


def test_weights_validation():
    valid_dec = {"interest_fit": 0.3, "academic_fit": 0.3, "financial_fit": 0.4}
    assert validate_weights(valid_dec) is True

    valid_pct = {"interest_fit": 30.0, "academic_fit": 30.0, "financial_fit": 40.0}
    assert validate_weights(valid_pct) is True

    invalid = {"interest_fit": 0.1, "academic_fit": 0.1}
    assert validate_weights(invalid) is False


def test_normalize_weights():
    pct_weights = {"interest_fit": 50.0, "academic_fit": 50.0}
    norm = normalize_weights(pct_weights)
    assert norm["interest_fit"] == 0.5
    assert norm["academic_fit"] == 0.5


def test_decision_matrix_ranking():
    pathways = [
        {
            "id": "p1",
            "name": "Pathway A (High Interest)",
            "interest_fit_score": 95.0,
            "academic_fit_score": 70.0,
            "financial_fit_score": 60.0,
            "compatibility_score": 80.0,
            "total_duration_years": 4.0
        },
        {
            "id": "p2",
            "name": "Pathway B (High Budget Fit)",
            "interest_fit_score": 60.0,
            "academic_fit_score": 75.0,
            "financial_fit_score": 98.0,
            "compatibility_score": 75.0,
            "total_duration_years": 3.0
        }
    ]

    # Prioritize Interest Fit (60%)
    interest_heavy_weights = {
        "interest_fit": 0.60,
        "academic_fit": 0.10,
        "financial_fit": 0.10,
        "career_alignment": 0.10,
        "location_fit": 0.05,
        "duration": 0.025,
        "flexibility": 0.025
    }
    result1 = calculate_matrix(pathways, interest_heavy_weights)
    assert result1["pathway_scores"][0]["pathway_id"] == "p1"

    # Prioritize Financial Fit (60%)
    budget_heavy_weights = {
        "interest_fit": 0.10,
        "academic_fit": 0.10,
        "financial_fit": 0.60,
        "career_alignment": 0.10,
        "location_fit": 0.05,
        "duration": 0.025,
        "flexibility": 0.025
    }
    result2 = calculate_matrix(pathways, budget_heavy_weights)
    assert result2["pathway_scores"][0]["pathway_id"] == "p2"
