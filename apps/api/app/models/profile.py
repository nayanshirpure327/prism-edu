from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, DateTime, Date
from sqlalchemy.dialects.postgresql import JSON
from .base import BaseModel

class StudentProfile(BaseModel):
    __tablename__ = "student_profiles"
    user_id = Column(ForeignKey("users.id"), unique=True)
    full_name = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)
    phone = Column(String)
    avatar_url = Column(String)
    bio = Column(String)
    city = Column(String)
    region = Column(String)
    country_code = Column(String)
    current_class = Column(String)
    board_system = Column(String)
    academic_year = Column(String)
    profile_completion_pct = Column(Integer, default=0)
    is_profile_complete = Column(Boolean, default=False)
    wizard_step = Column(Integer, default=1)

class AcademicRecord(BaseModel):
    __tablename__ = "academic_records"
    student_profile_id = Column(ForeignKey("student_profiles.id"))
    subject_name = Column(String)
    marks_obtained = Column(Float)
    max_marks = Column(Float)
    percentage = Column(Float)
    grade = Column(String)
    academic_year = Column(String)
    term = Column(String)
    board = Column(String)

class WorkPreference(BaseModel):
    __tablename__ = "work_preferences"
    student_profile_id = Column(ForeignKey("student_profiles.id"))
    work_style = Column(String)
    work_environment = Column(String)
    work_setting = Column(String)
    people_technology = Column(String)
    research_interest = Column(Boolean)
    stable_employment = Column(Boolean)
    entrepreneurship = Column(Boolean)
    remote_preference = Column(Boolean)
    travel_willingness = Column(Boolean)
    annual_budget_min = Column(Float)
    annual_budget_max = Column(Float)
    budget_currency = Column(String)
    family_contribution = Column(Float)
    savings = Column(Float)
    scholarship_expectation = Column(Boolean)
    loan_willingness = Column(Boolean)
    max_loan_amount = Column(Float)
    comfortable_monthly_repayment = Column(Float)
    preferred_countries = Column(JSON)
    relocation_preference = Column(Boolean)
    online_study_preference = Column(Boolean)

class ParentStudentLink(BaseModel):
    __tablename__ = "parent_student_links"
    parent_user_id = Column(ForeignKey("users.id"))
    student_profile_id = Column(ForeignKey("student_profiles.id"))
    consent_given_at = Column(DateTime)
    relationship_type = Column(String)
    is_active = Column(Boolean, default=True)

class CounselorStudentAssignment(BaseModel):
    __tablename__ = "counselor_student_assignments"
    counselor_user_id = Column(ForeignKey("users.id"))
    student_profile_id = Column(ForeignKey("student_profiles.id"))
    assigned_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
