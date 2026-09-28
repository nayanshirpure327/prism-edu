import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../apps/api")))

from app.domains.pathways.engine import PathwayEngine


def test_pathway_hard_constraint_enforcement():
    engine = PathwayEngine()

    medical_career = {
        "id": "c_doc",
        "name": "Medical Doctor (MBBS)",
        "slug": "medical-doctor",
        "related_subjects": ["Biology", "Chemistry", "Physics"],
        "is_licensed": True
    }

    # Student has PCM (No Biology)
    student_academic_no_bio = {"subjects": ["Physics", "Chemistry", "Mathematics"]}
    prefs = {"annual_budget_max": 500000}

    eval_result = engine.evaluate_constraints(medical_career, student_academic_no_bio, prefs)
    assert eval_result["hard_constraints_met"] is False
    assert eval_result["constraint_status"] == "REQUIRES_ADJUSTMENT"
    assert any("Biology" in issue for issue in eval_result["missing_mandatory_prerequisites"])

    # Student with Biology
    student_academic_with_bio = {"subjects": ["Physics", "Chemistry", "Biology", "English"]}
    eval_result_ok = engine.evaluate_constraints(medical_career, student_academic_with_bio, prefs)
    assert eval_result_ok["hard_constraints_met"] is True
    assert eval_result_ok["constraint_status"] == "COMPATIBLE"


def test_pathway_soft_constraint_budget_flagging():
    engine = PathwayEngine()

    eng_career = {
        "id": "c_eng",
        "name": "Software Engineer",
        "slug": "software-engineer",
        "related_subjects": ["Mathematics", "Computer Science"],
        "avg_tuition_annual": 250000,
        "is_licensed": False
    }

    student_academic = {"subjects": ["Physics", "Chemistry", "Mathematics"]}
    # Budget is 100,000 (less than 250,000)
    low_budget_prefs = {"annual_budget_max": 100000}

    eval_result = engine.evaluate_constraints(eng_career, student_academic, low_budget_prefs)
    assert eval_result["hard_constraints_met"] is True
    assert eval_result["constraint_status"] == "POTENTIAL_CHALLENGE"
    assert len(eval_result["soft_constraint_issues"]) > 0


def test_candidate_pathway_generation_structure():
    engine = PathwayEngine()
    career = {
        "id": "c_cs",
        "name": "Data Scientist",
        "slug": "data-scientist",
        "related_subjects": ["Mathematics", "Statistics"],
        "is_licensed": False,
        "career_type": "Technology"
    }
    profile = {"current_class": "12", "school_name": "Delhi Public School"}
    academic = {"subjects": ["Mathematics", "Statistics", "Computer Science"]}
    prefs = {"annual_budget_max": 200000}

    pathway = engine.generate_candidate_pathway(career, profile, academic, prefs)
    assert pathway["career_name"] == "Data Scientist"
    assert pathway["total_duration_years"] >= 4
    assert len(pathway["steps"]) >= 3
    assert pathway["estimated_total_cost"] > 0
    assert len(pathway["assumptions"]) > 0
    assert len(pathway["uncertainties"]) > 0
