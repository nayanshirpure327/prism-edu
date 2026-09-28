from sqlalchemy import Column, String, Boolean, Float, Integer, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSON, UUID
import enum
from .base import BaseModel

class PathwayStatus(enum.Enum):
    DRAFT = "DRAFT"
    GENERATED = "GENERATED"
    SAVED = "SAVED"
    ARCHIVED = "ARCHIVED"

class Pathway(BaseModel):
    __tablename__ = "pathways"
    student_profile_id = Column(ForeignKey("student_profiles.id"))
    name = Column(String)
    description = Column(String)
    status = Column(SQLEnum(PathwayStatus))
    total_duration_years = Column(Float)
    estimated_total_cost = Column(Float)
    cost_currency = Column(String)
    career_id = Column(ForeignKey("careers.id"), nullable=True)
    career_name = Column(String)
    compatibility_score = Column(Float)
    interest_fit_score = Column(Float)
    academic_fit_score = Column(Float)
    financial_fit_score = Column(Float)
    constraint_status = Column(String)
    hard_constraints_met = Column(Boolean)
    soft_constraint_issues = Column(JSON)
    ai_explanation = Column(String)
    assumptions = Column(JSON)
    uncertainties = Column(JSON)
    is_primary = Column(Boolean, default=False)
    generated_at = Column(DateTime)

class PathwayStep(BaseModel):
    __tablename__ = "pathway_steps"
    pathway_id = Column(ForeignKey("pathways.id"))
    step_order = Column(Integer)
    step_type = Column(String)
    title = Column(String)
    description = Column(String)
    institution_name = Column(String)
    institution_id = Column(ForeignKey("institutions.id"), nullable=True)
    program_id = Column(ForeignKey("programs.id"), nullable=True)
    duration_months = Column(Integer)
    cost_estimate = Column(Float)
    cost_currency = Column(String)
    is_required = Column(Boolean)
    start_year_offset = Column(Float)
    end_year_offset = Column(Float)
    notes = Column(String)

class Scenario(BaseModel):
    __tablename__ = "scenarios"
    student_profile_id = Column(ForeignKey("student_profiles.id"))
    name = Column(String)
    description = Column(String)
    is_base_scenario = Column(Boolean, default=False)
    parent_scenario_id = Column(ForeignKey("scenarios.id"), nullable=True)
    version = Column(Integer)
    changes_summary = Column(JSON)

class ScenarioChange(BaseModel):
    __tablename__ = "scenario_changes"
    scenario_id = Column(ForeignKey("scenarios.id"))
    change_type = Column(String)
    field_name = Column(String)
    old_value = Column(JSON)
    new_value = Column(JSON)
    changed_at = Column(DateTime)

class DecisionMatrixResult(BaseModel):
    __tablename__ = "decision_matrix_results"
    student_profile_id = Column(ForeignKey("student_profiles.id"))
    name = Column(String)
    weights = Column(JSON)
    pathway_scores = Column(JSON)

class Report(BaseModel):
    __tablename__ = "reports"
    student_profile_id = Column(ForeignKey("student_profiles.id"))
    report_type = Column(String)
    title = Column(String)
    status = Column(String)
    file_url = Column(String)
    file_size_bytes = Column(Integer)
    generated_at = Column(DateTime)
    expires_at = Column(DateTime)

class Notification(BaseModel):
    __tablename__ = "notifications"
    user_id = Column(ForeignKey("users.id"))
    title = Column(String)
    message = Column(String)
    notification_type = Column(String)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    action_url = Column(String, nullable=True)

class AuditLog(BaseModel):
    __tablename__ = "audit_logs"
    user_id = Column(ForeignKey("users.id"), nullable=True)
    entity_type = Column(String)
    entity_id = Column(UUID(as_uuid=True))
    action = Column(String)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
