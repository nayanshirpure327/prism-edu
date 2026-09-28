from sqlalchemy import Column, String, Boolean, Float, Integer, ForeignKey, DateTime, Date, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSON
from .base import BaseModel
from .user import DataStatus

class Country(BaseModel):
    __tablename__ = "countries"
    code = Column(String)
    name = Column(String)
    currency_code = Column(String)

class EducationSystem(BaseModel):
    __tablename__ = "education_systems"
    country_id = Column(ForeignKey("countries.id"))
    name = Column(String)
    description = Column(String)
    levels = Column(JSON)

class Institution(BaseModel):
    __tablename__ = "institutions"
    name = Column(String)
    slug = Column(String, unique=True)
    type = Column(String)
    country_id = Column(ForeignKey("countries.id"))
    city = Column(String)
    region = Column(String)
    established_year = Column(Integer)
    ranking_global = Column(Integer, nullable=True)
    ranking_national = Column(Integer, nullable=True)
    accreditation = Column(String)
    website = Column(String)
    email = Column(String)
    phone = Column(String)
    description = Column(String)
    logo_url = Column(String)
    image_url = Column(String)
    is_active = Column(Boolean, default=True)
    data_status = Column(SQLEnum(DataStatus), default=DataStatus.ESTIMATED)
    verified_at = Column(DateTime, nullable=True)
    source_url = Column(String, nullable=True)

class Program(BaseModel):
    __tablename__ = "programs"
    institution_id = Column(ForeignKey("institutions.id"))
    name = Column(String)
    slug = Column(String)
    degree_level = Column(String)
    field_of_study = Column(String)
    duration_years = Column(Float)
    total_seats = Column(Integer, nullable=True)
    tuition_fee_per_year = Column(Float)
    tuition_currency = Column(String)
    living_cost_estimate_per_year = Column(Float)
    application_fee = Column(Float)
    language_of_instruction = Column(String)
    intake_months = Column(JSON)
    application_deadline = Column(String)
    minimum_percentage = Column(Float)
    minimum_grade = Column(String)
    entrance_exam_required = Column(Boolean, default=False)
    entrance_exams = Column(JSON)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    data_status = Column(SQLEnum(DataStatus), default=DataStatus.ESTIMATED)
    verified_at = Column(DateTime, nullable=True)
    source_url = Column(String, nullable=True)

class ProgramRequirement(BaseModel):
    __tablename__ = "program_requirements"
    program_id = Column(ForeignKey("programs.id"))
    requirement_type = Column(String)
    requirement_name = Column(String)
    is_mandatory = Column(Boolean)
    details = Column(String)

class Scholarship(BaseModel):
    __tablename__ = "scholarships"
    name = Column(String)
    slug = Column(String, unique=True)
    provider = Column(String)
    country_id = Column(ForeignKey("countries.id"), nullable=True)
    amount_per_year = Column(Float)
    max_amount = Column(Float)
    coverage_type = Column(String)
    currency = Column(String)
    deadline = Column(Date, nullable=True)
    description = Column(String)
    eligibility_academic_min_percentage = Column(Float, nullable=True)
    eligibility_financial_need = Column(Boolean, default=False)
    citizenship_requirement = Column(JSON)
    is_renewable = Column(Boolean, default=False)
    renewable_conditions = Column(String)
    application_url = Column(String)
    is_active = Column(Boolean, default=True)
    data_status = Column(SQLEnum(DataStatus), default=DataStatus.ESTIMATED)
    verified_at = Column(DateTime, nullable=True)
    source_url = Column(String, nullable=True)

class LoanProduct(BaseModel):
    __tablename__ = "loan_products"
    name = Column(String)
    provider = Column(String)
    loan_type = Column(String)
    country_id = Column(ForeignKey("countries.id"))
    min_amount = Column(Float)
    max_amount = Column(Float)
    currency = Column(String)
    interest_rate_min = Column(Float)
    interest_rate_max = Column(Float)
    rate_type = Column(String)
    max_tenure_months = Column(Integer)
    moratorium_months = Column(Integer)
    processing_fee_pct = Column(Float)
    collateral_required = Column(Boolean)
    co_borrower_required = Column(Boolean)
    description = Column(String)
    eligibility_criteria = Column(String)
    application_url = Column(String)
    is_active = Column(Boolean, default=True)
    data_status = Column(SQLEnum(DataStatus), default=DataStatus.ESTIMATED)
    verified_at = Column(DateTime, nullable=True)
    source_url = Column(String, nullable=True)
