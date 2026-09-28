from typing import List, Dict, Any, Optional
import uuid


class PathwayEngine:
    """
    Deterministic Pathway Generation Engine.
    Combines student academic record, constraints, and career knowledge graph.
    """

    def evaluate_constraints(self, target_career: Dict[str, Any], student_academic: Dict[str, Any], preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check hard and soft constraints.
        Hard: prerequisite subjects (e.g. Biology for MBBS, Physics+Math for Engineering).
        Soft: budget, location, mode.
        """
        subjects_taken = [s.lower() for s in student_academic.get("subjects", [])]
        req_subjects = [s.lower() for s in target_career.get("related_subjects", [])]

        hard_met = True
        missing_mandatory = []

        career_slug = target_career.get("slug", "").lower()
        if "doctor" in career_slug or "medical" in career_slug:
            if "biology" not in subjects_taken:
                hard_met = False
                missing_mandatory.append("Biology (Mandatory for Medical qualification)")
        elif "engineer" in career_slug:
            if "mathematics" not in subjects_taken and "math" not in subjects_taken:
                hard_met = False
                missing_mandatory.append("Mathematics (Mandatory for Engineering qualification)")

        # Soft constraints
        soft_issues = []
        budget_max = float(preferences.get("annual_budget_max") or 0.0)
        est_tuition = float(target_career.get("avg_tuition_annual") or 120000.0)
        if budget_max > 0 and est_tuition > budget_max:
            soft_issues.append(f"Estimated annual tuition (₹{est_tuition:,.0f}) exceeds your preferred budget limit of ₹{budget_max:,.0f}. Scholarship or education loan recommended.")

        if not hard_met:
            status = "REQUIRES_ADJUSTMENT"
        elif soft_issues:
            status = "POTENTIAL_CHALLENGE"
        else:
            status = "COMPATIBLE"

        return {
            "hard_constraints_met": hard_met,
            "missing_mandatory_prerequisites": missing_mandatory,
            "soft_constraint_issues": soft_issues,
            "constraint_status": status
        }

    def generate_candidate_pathway(
        self,
        career: Dict[str, Any],
        student_profile: Dict[str, Any],
        academic_record: Dict[str, Any],
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesizes a complete multi-step pathway for a target career.
        """
        constraint_eval = self.evaluate_constraints(career, academic_record, preferences)

        edu_paths = career.get("typical_education_paths") or []
        steps = []
        step_order = 1
        curr_year = 0

        # Step 1: Senior Secondary / Preparatory
        steps.append({
            "step_order": step_order,
            "step_type": "qualification",
            "title": f"Complete Senior Secondary ({student_profile.get('current_class', '12')}th)",
            "description": f"Focus on core disciplines: {', '.join(career.get('related_subjects', ['Core Subjects']))}",
            "institution_name": student_profile.get("school_name", "Senior Secondary School"),
            "duration_months": 12,
            "cost_estimate": 40000.0,
            "cost_currency": "INR",
            "is_required": True,
            "start_year_offset": curr_year,
            "end_year_offset": curr_year + 1
        })
        curr_year += 1
        step_order += 1

        # Step 2: Entrance / Gateway Exam (if licensed/technical)
        if career.get("is_licensed") or "engineer" in career.get("slug", "") or "doctor" in career.get("slug", ""):
            exam_name = "NEET UG" if "doctor" in career.get("slug", "") else "JEE Main / State CET"
            steps.append({
                "step_order": step_order,
                "step_type": "exam",
                "title": f"Qualify Entrance Exam: {exam_name}",
                "description": f"National or state-level entrance examination for admission into recognized institutions.",
                "institution_name": "National Testing Agency / State Board",
                "duration_months": 6,
                "cost_estimate": 5000.0,
                "cost_currency": "INR",
                "is_required": True,
                "start_year_offset": curr_year - 1,
                "end_year_offset": curr_year
            })
            step_order += 1

        # Step 3: Degree Program
        deg_duration = 5.5 if "doctor" in career.get("slug", "") else 4 if "engineer" in career.get("slug", "") else 3
        prog_title = "MBBS" if "doctor" in career.get("slug", "") else f"Bachelor of Technology / B.Sc in {career.get('name')}"
        annual_cost = 150000.0 if "doctor" in career.get("slug", "") else 120000.0

        steps.append({
            "step_order": step_order,
            "step_type": "program",
            "title": prog_title,
            "description": f"Accredited professional degree covering theoretical foundations, laboratory experiments, and industrial capstone projects.",
            "institution_name": "Accredited University / Institute",
            "duration_months": int(deg_duration * 12),
            "cost_estimate": annual_cost * deg_duration,
            "cost_currency": "INR",
            "is_required": True,
            "start_year_offset": curr_year,
            "end_year_offset": curr_year + int(deg_duration)
        })
        curr_year += int(deg_duration)
        step_order += 1

        # Step 4: Practical Internship / Industry Entry
        steps.append({
            "step_order": step_order,
            "step_type": "work_experience",
            "title": f"Entry-level Role: Associate / Junior {career.get('name')}",
            "description": f"Apply theoretical knowledge in real industry environments and develop production-grade competency.",
            "institution_name": f"Leading {career.get('career_type', 'Industry')} Enterprise / Clinical Center",
            "duration_months": 12,
            "cost_estimate": 0.0,
            "cost_currency": "INR",
            "is_required": True,
            "start_year_offset": curr_year,
            "end_year_offset": curr_year + 1
        })

        total_est_cost = sum(s["cost_estimate"] for s in steps)
        total_duration = curr_year

        # Compute transparent fit scores
        academic_score = 85.0 if constraint_eval["hard_constraints_met"] else 40.0
        interest_score = 88.0
        financial_score = 90.0 if not constraint_eval["soft_constraint_issues"] else 65.0
        compat_score = round((academic_score * 0.4 + interest_score * 0.4 + financial_score * 0.2), 1)

        return {
            "id": str(uuid.uuid4()),
            "name": f"Direct Academic Route to {career.get('name')}",
            "description": f"Structured pathway starting from senior secondary through higher education into career launch as a {career.get('name')}.",
            "career_id": career.get("id"),
            "career_name": career.get("name"),
            "total_duration_years": total_duration,
            "estimated_total_cost": total_est_cost,
            "cost_currency": "INR",
            "compatibility_score": compat_score,
            "academic_fit_score": academic_score,
            "interest_fit_score": interest_score,
            "financial_fit_score": financial_score,
            "constraint_status": constraint_eval["constraint_status"],
            "hard_constraints_met": constraint_eval["hard_constraints_met"],
            "soft_constraint_issues": constraint_eval["soft_constraint_issues"],
            "steps": steps,
            "assumptions": [
                "Assumes continuous enrollment and timely graduation without academic hiatus",
                "Fee projections are based on current baseline tuition figures and average inflationary trends"
            ],
            "uncertainties": [
                "Entrance exam cut-offs fluctuate by year based on applicant percentiles",
                "Living cost varies widely depending on host city tier"
            ]
        }
