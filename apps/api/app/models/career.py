from sqlalchemy import Column, String, Boolean, Float, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSON, UUID
from .base import BaseModel
from .user import DataStatus

class Industry(BaseModel):
    __tablename__ = "industries"
    name = Column(String)
    slug = Column(String, unique=True)
    description = Column(String)
    icon = Column(String)

class Skill(BaseModel):
    __tablename__ = "skills"
    name = Column(String)
    slug = Column(String, unique=True)
    category = Column(String)
    level_required = Column(String)

class Career(BaseModel):
    __tablename__ = "careers"
    name = Column(String)
    slug = Column(String, unique=True)
    description = Column(String)
    industry_id = Column(ForeignKey("industries.id"))
    education_level_required = Column(String)
    avg_salary_min = Column(Float)
    avg_salary_max = Column(Float)
    salary_currency = Column(String)
    growth_outlook = Column(String)
    is_licensed = Column(Boolean, default=False)
    license_info = Column(String)
    related_subjects = Column(JSON)
    required_skills = Column(JSON)
    typical_education_paths = Column(JSON)
    work_environment = Column(String)
    career_type = Column(String)
    is_active = Column(Boolean, default=True)
    data_status = Column(SQLEnum(DataStatus), default=DataStatus.ESTIMATED)
    verified_at = Column(DateTime, nullable=True)
    source_url = Column(String, nullable=True)
    review_due_at = Column(DateTime, nullable=True)

class CareerSkill(BaseModel):
    __tablename__ = "career_skills"
    career_id = Column(ForeignKey("careers.id"))
    skill_id = Column(ForeignKey("skills.id"))
    importance = Column(String)

class SavedItem(BaseModel):
    __tablename__ = "saved_items"
    user_id = Column(ForeignKey("users.id"))
    item_type = Column(String)
    item_id = Column(UUID(as_uuid=True))
    saved_at = Column(DateTime)
