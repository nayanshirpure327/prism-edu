import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../apps/api")))

from app.domains.assessments.scoring import (
    score_aptitude_assessment,
    score_interest_assessment,
    compute_top_aptitudes,
    compute_recommended_streams
)


def test_aptitude_scoring():
    questions = [
        {"id": "q1", "category": "logical_reasoning", "options": [{"score": 3}, {"score": 0}]},
        {"id": "q2", "category": "numerical", "options": [{"score": 3}, {"score": 0}]},
        {"id": "q3", "category": "verbal", "options": [{"score": 3}, {"score": 0}]},
    ]
    answers = [
        {"question_id": "q1", "raw_score": 3},
        {"question_id": "q2", "raw_score": 1.5},
        {"question_id": "q3", "raw_score": 0},
    ]

    scores = score_aptitude_assessment(answers, questions)
    assert scores["logical"] == 100.0
    assert scores["numerical"] == 50.0
    assert scores["verbal"] == 0.0

    top = compute_top_aptitudes(scores)
    assert top[0] == "logical"
    assert top[1] == "numerical"


def test_interest_scoring():
    questions = [
        {"id": "iq1", "category": "technology"},
        {"id": "iq2", "category": "technology"},
        {"id": "iq3", "category": "science"},
    ]
    # Rating scale: 1 to 5
    answers = [
        {"question_id": "iq1", "raw_score": 5},
        {"question_id": "iq2", "raw_score": 5},
        {"question_id": "iq3", "raw_score": 3},
    ]

    scores = score_interest_assessment(answers, questions)
    assert scores["technology"] == 100.0
    assert scores["science"] == 50.0


def test_recommended_streams_generation():
    interest_scores = {
        "technology": 90.0,
        "science": 85.0,
        "commerce": 30.0,
        "arts": 20.0,
        "social": 40.0,
        "creative": 50.0
    }
    aptitude_scores = {
        "numerical": 80.0,
        "logical": 85.0,
        "verbal": 60.0,
        "spatial": 70.0,
        "analytical": 75.0
    }

    streams = compute_recommended_streams(interest_scores, aptitude_scores)
    assert len(streams) >= 3
    # Top stream should be STEM / Engineering given tech=90, sci=85, num=80, log=85
    assert "Science (PCM - Engineering & Technology)" in streams[0]["stream"]
    assert streams[0]["fit_score"] > 80.0
