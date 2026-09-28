from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Enum as SQLEnum, DateTime, Float
from sqlalchemy.dialects.postgresql import JSON
import enum
from .base import BaseModel

class AssessmentType(enum.Enum):
    APTITUDE = "APTITUDE"
    INTEREST = "INTEREST"
    PERSONALITY = "PERSONALITY"

class QuestionType(enum.Enum):
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    RATING_SCALE = "RATING_SCALE"
    RANKING = "RANKING"
    BOOLEAN = "BOOLEAN"

class Assessment(BaseModel):
    __tablename__ = "assessments"
    name = Column(String)
    description = Column(String)
    type = Column(SQLEnum(AssessmentType))
    version = Column(String)
    total_questions = Column(Integer)
    time_limit_minutes = Column(Integer)
    is_active = Column(Boolean, default=True)

class AssessmentQuestion(BaseModel):
    __tablename__ = "assessment_questions"
    assessment_id = Column(ForeignKey("assessments.id"))
    question_text = Column(String)
    question_type = Column(SQLEnum(QuestionType))
    category = Column(String)
    options = Column(JSON)
    correct_option_index = Column(Integer, nullable=True)
    order_index = Column(Integer)
    weight = Column(Float, default=1.0)

class AssessmentAttempt(BaseModel):
    __tablename__ = "assessment_attempts"
    student_profile_id = Column(ForeignKey("student_profiles.id"))
    assessment_id = Column(ForeignKey("assessments.id"))
    started_at = Column(DateTime)
    completed_at = Column(DateTime, nullable=True)
    time_taken_seconds = Column(Integer, nullable=True)
    is_complete = Column(Boolean, default=False)
    attempt_number = Column(Integer)

class AssessmentAnswer(BaseModel):
    __tablename__ = "assessment_answers"
    attempt_id = Column(ForeignKey("assessment_attempts.id"))
    question_id = Column(ForeignKey("assessment_questions.id"))
    selected_option = Column(String)
    raw_score = Column(Float, nullable=True)

class AssessmentResult(BaseModel):
    __tablename__ = "assessment_results"
    attempt_id = Column(ForeignKey("assessment_attempts.id"))
    student_profile_id = Column(ForeignKey("student_profiles.id"))
    assessment_id = Column(ForeignKey("assessments.id"))
    aptitude_scores = Column(JSON)
    interest_scores = Column(JSON)
    top_aptitudes = Column(JSON)
    top_interests = Column(JSON)
    recommended_streams = Column(JSON)
    overall_summary = Column(String)
    computed_at = Column(DateTime)
