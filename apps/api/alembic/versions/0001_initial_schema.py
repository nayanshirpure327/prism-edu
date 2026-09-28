"""Initial Schema — All PRISM-EDU tables

Revision ID: 0001
Revises:
Create Date: 2026-09-27
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # pgvector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')

    # ── Enums ───────────────────────────────────────────────
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE userrole AS ENUM ('STUDENT','PARENT','COUNSELOR','ADMIN');
        EXCEPTION WHEN duplicate_object THEN null; END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE datastatus AS ENUM (
                'VERIFIED','NEEDS_VERIFICATION','EXPIRED','HISTORICAL','ESTIMATED','USER_PROVIDED'
            );
        EXCEPTION WHEN duplicate_object THEN null; END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE assessmenttype AS ENUM ('APTITUDE','INTEREST','PERSONALITY');
        EXCEPTION WHEN duplicate_object THEN null; END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE pathwaystatus AS ENUM ('DRAFT','GENERATED','SAVED','ARCHIVED');
        EXCEPTION WHEN duplicate_object THEN null; END $$;
    """)

    # ── users ─────────────────────────────────────────────
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('role', sa.Enum('STUDENT','PARENT','COUNSELOR','ADMIN', name='userrole'), nullable=False, server_default='STUDENT'),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100), nullable=False),
        sa.Column('is_active', sa.Boolean, server_default='true'),
        sa.Column('is_email_verified', sa.Boolean, server_default='false'),
        sa.Column('email_verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_users_email', 'users', ['email'])

    # ── refresh_tokens ────────────────────────────────────
    op.create_table('refresh_tokens',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('token_hash', sa.String(255), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('ip_address', sa.String(50), nullable=True),
        sa.Column('user_agent', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── countries ─────────────────────────────────────────
    op.create_table('countries',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('code', sa.String(3), nullable=False, unique=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('currency_code', sa.String(10), nullable=False, server_default='USD'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── student_profiles ──────────────────────────────────
    op.create_table('student_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('full_name', sa.String(200), nullable=True),
        sa.Column('date_of_birth', sa.Date, nullable=True),
        sa.Column('gender', sa.String(30), nullable=True),
        sa.Column('phone', sa.String(30), nullable=True),
        sa.Column('avatar_url', sa.String(500), nullable=True),
        sa.Column('bio', sa.Text, nullable=True),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('region', sa.String(100), nullable=True),
        sa.Column('country_code', sa.String(3), nullable=True),
        sa.Column('current_class', sa.String(20), nullable=True),
        sa.Column('board_system', sa.String(50), nullable=True),
        sa.Column('academic_year', sa.String(20), nullable=True),
        sa.Column('profile_completion_pct', sa.Integer, server_default='0'),
        sa.Column('is_profile_complete', sa.Boolean, server_default='false'),
        sa.Column('wizard_step', sa.Integer, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_student_profiles_user_id', 'student_profiles', ['user_id'])

    # ── academic_records ──────────────────────────────────
    op.create_table('academic_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('student_profile_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('subject_name', sa.String(100), nullable=False),
        sa.Column('marks_obtained', sa.Float, nullable=True),
        sa.Column('max_marks', sa.Float, nullable=True),
        sa.Column('percentage', sa.Float, nullable=True),
        sa.Column('grade', sa.String(10), nullable=True),
        sa.Column('academic_year', sa.String(20), nullable=True),
        sa.Column('term', sa.String(20), nullable=True),
        sa.Column('board', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── work_preferences ─────────────────────────────────
    op.create_table('work_preferences',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('student_profile_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('work_style', sa.String(30), nullable=True),
        sa.Column('work_environment', sa.String(30), nullable=True),
        sa.Column('work_setting', sa.String(30), nullable=True),
        sa.Column('people_technology', sa.String(30), nullable=True),
        sa.Column('research_interest', sa.Boolean, server_default='false'),
        sa.Column('stable_employment', sa.Boolean, server_default='true'),
        sa.Column('entrepreneurship', sa.Boolean, server_default='false'),
        sa.Column('remote_preference', sa.Boolean, server_default='false'),
        sa.Column('travel_willingness', sa.Boolean, server_default='false'),
        sa.Column('annual_budget_min', sa.Float, nullable=True),
        sa.Column('annual_budget_max', sa.Float, nullable=True),
        sa.Column('budget_currency', sa.String(10), server_default='INR'),
        sa.Column('family_contribution', sa.Float, nullable=True),
        sa.Column('savings', sa.Float, nullable=True),
        sa.Column('scholarship_expectation', sa.Boolean, server_default='false'),
        sa.Column('loan_willingness', sa.Boolean, server_default='false'),
        sa.Column('max_loan_amount', sa.Float, nullable=True),
        sa.Column('comfortable_monthly_repayment', sa.Float, nullable=True),
        sa.Column('preferred_countries', postgresql.JSONB, server_default='[]'),
        sa.Column('relocation_preference', sa.Boolean, server_default='false'),
        sa.Column('online_study_preference', sa.Boolean, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── industries ────────────────────────────────────────
    op.create_table('industries',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('slug', sa.String(100), nullable=False, unique=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('icon', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── skills ────────────────────────────────────────────
    op.create_table('skills',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('slug', sa.String(100), nullable=False, unique=True),
        sa.Column('category', sa.String(50), nullable=True),
        sa.Column('level_required', sa.String(30), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── careers ───────────────────────────────────────────
    op.create_table('careers',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('slug', sa.String(200), nullable=False, unique=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('industry_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('industries.id'), nullable=True),
        sa.Column('education_level_required', sa.String(50), nullable=True),
        sa.Column('avg_salary_min', sa.Float, nullable=True),
        sa.Column('avg_salary_max', sa.Float, nullable=True),
        sa.Column('salary_currency', sa.String(10), server_default='INR'),
        sa.Column('growth_outlook', sa.String(20), nullable=True),
        sa.Column('is_licensed', sa.Boolean, server_default='false'),
        sa.Column('license_info', sa.Text, nullable=True),
        sa.Column('related_subjects', postgresql.JSONB, server_default='[]'),
        sa.Column('required_skills', postgresql.JSONB, server_default='[]'),
        sa.Column('typical_education_paths', postgresql.JSONB, server_default='[]'),
        sa.Column('work_environment', sa.String(50), nullable=True),
        sa.Column('career_type', sa.String(50), nullable=True),
        sa.Column('is_active', sa.Boolean, server_default='true'),
        sa.Column('data_status', sa.Enum('VERIFIED','NEEDS_VERIFICATION','EXPIRED','HISTORICAL','ESTIMATED','USER_PROVIDED', name='datastatus'), server_default='NEEDS_VERIFICATION'),
        sa.Column('verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('source_url', sa.String(500), nullable=True),
        sa.Column('review_due_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_careers_slug', 'careers', ['slug'])
    op.create_index('ix_careers_industry_id', 'careers', ['industry_id'])
    op.create_index('ix_careers_is_active', 'careers', ['is_active'])

    # ── institutions ──────────────────────────────────────
    op.create_table('institutions',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('name', sa.String(300), nullable=False),
        sa.Column('slug', sa.String(300), nullable=False, unique=True),
        sa.Column('type', sa.String(50), nullable=True),
        sa.Column('country_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('countries.id'), nullable=True),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('region', sa.String(100), nullable=True),
        sa.Column('established_year', sa.Integer, nullable=True),
        sa.Column('ranking_global', sa.Integer, nullable=True),
        sa.Column('ranking_national', sa.Integer, nullable=True),
        sa.Column('accreditation', sa.String(200), nullable=True),
        sa.Column('website', sa.String(500), nullable=True),
        sa.Column('email', sa.String(200), nullable=True),
        sa.Column('phone', sa.String(50), nullable=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('logo_url', sa.String(500), nullable=True),
        sa.Column('image_url', sa.String(500), nullable=True),
        sa.Column('is_active', sa.Boolean, server_default='true'),
        sa.Column('data_status', sa.Enum('VERIFIED','NEEDS_VERIFICATION','EXPIRED','HISTORICAL','ESTIMATED','USER_PROVIDED', name='datastatus'), server_default='NEEDS_VERIFICATION'),
        sa.Column('verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('source_url', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_institutions_slug', 'institutions', ['slug'])
    op.create_index('ix_institutions_country_id', 'institutions', ['country_id'])

    # ── programs ──────────────────────────────────────────
    op.create_table('programs',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('institution_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('institutions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(300), nullable=False),
        sa.Column('slug', sa.String(300), nullable=False),
        sa.Column('degree_level', sa.String(50), nullable=True),
        sa.Column('field_of_study', sa.String(200), nullable=True),
        sa.Column('duration_years', sa.Float, nullable=True),
        sa.Column('total_seats', sa.Integer, nullable=True),
        sa.Column('tuition_fee_per_year', sa.Float, nullable=True),
        sa.Column('tuition_currency', sa.String(10), server_default='INR'),
        sa.Column('living_cost_estimate_per_year', sa.Float, nullable=True),
        sa.Column('application_fee', sa.Float, nullable=True),
        sa.Column('language_of_instruction', sa.String(50), server_default='English'),
        sa.Column('intake_months', postgresql.JSONB, server_default='[]'),
        sa.Column('application_deadline', sa.String(100), nullable=True),
        sa.Column('minimum_percentage', sa.Float, nullable=True),
        sa.Column('minimum_grade', sa.String(10), nullable=True),
        sa.Column('entrance_exam_required', sa.Boolean, server_default='false'),
        sa.Column('entrance_exams', postgresql.JSONB, server_default='[]'),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('is_active', sa.Boolean, server_default='true'),
        sa.Column('data_status', sa.Enum('VERIFIED','NEEDS_VERIFICATION','EXPIRED','HISTORICAL','ESTIMATED','USER_PROVIDED', name='datastatus'), server_default='NEEDS_VERIFICATION'),
        sa.Column('verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('source_url', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_programs_institution_id', 'programs', ['institution_id'])

    # ── scholarships ──────────────────────────────────────
    op.create_table('scholarships',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('name', sa.String(300), nullable=False),
        sa.Column('slug', sa.String(300), nullable=False, unique=True),
        sa.Column('provider', sa.String(200), nullable=False),
        sa.Column('country_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('countries.id'), nullable=True),
        sa.Column('amount_per_year', sa.Float, nullable=True),
        sa.Column('max_amount', sa.Float, nullable=True),
        sa.Column('coverage_type', sa.String(50), nullable=True),
        sa.Column('currency', sa.String(10), server_default='INR'),
        sa.Column('deadline', sa.Date, nullable=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('eligibility_academic_min_percentage', sa.Float, nullable=True),
        sa.Column('eligibility_financial_need', sa.Boolean, server_default='false'),
        sa.Column('citizenship_requirement', postgresql.JSONB, server_default='[]'),
        sa.Column('is_renewable', sa.Boolean, server_default='false'),
        sa.Column('renewable_conditions', sa.Text, nullable=True),
        sa.Column('application_url', sa.String(500), nullable=True),
        sa.Column('is_active', sa.Boolean, server_default='true'),
        sa.Column('data_status', sa.Enum('VERIFIED','NEEDS_VERIFICATION','EXPIRED','HISTORICAL','ESTIMATED','USER_PROVIDED', name='datastatus'), server_default='NEEDS_VERIFICATION'),
        sa.Column('verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('source_url', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )

    # ── loan_products ─────────────────────────────────────
    op.create_table('loan_products',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('provider', sa.String(200), nullable=False),
        sa.Column('loan_type', sa.String(50), nullable=True),
        sa.Column('country_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('countries.id'), nullable=True),
        sa.Column('min_amount', sa.Float, nullable=True),
        sa.Column('max_amount', sa.Float, nullable=True),
        sa.Column('currency', sa.String(10), server_default='INR'),
        sa.Column('interest_rate_min', sa.Float, nullable=True),
        sa.Column('interest_rate_max', sa.Float, nullable=True),
        sa.Column('rate_type', sa.String(20), server_default='fixed'),
        sa.Column('max_tenure_months', sa.Integer, nullable=True),
        sa.Column('moratorium_months', sa.Integer, server_default='12'),
        sa.Column('processing_fee_pct', sa.Float, server_default='0'),
        sa.Column('collateral_required', sa.Boolean, server_default='false'),
        sa.Column('co_borrower_required', sa.Boolean, server_default='false'),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('eligibility_criteria', sa.Text, nullable=True),
        sa.Column('application_url', sa.String(500), nullable=True),
        sa.Column('is_active', sa.Boolean, server_default='true'),
        sa.Column('data_status', sa.Enum('VERIFIED','NEEDS_VERIFICATION','EXPIRED','HISTORICAL','ESTIMATED','USER_PROVIDED', name='datastatus'), server_default='NEEDS_VERIFICATION'),
        sa.Column('verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('source_url', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── assessments ───────────────────────────────────────
    op.create_table('assessments',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('type', sa.Enum('APTITUDE','INTEREST','PERSONALITY', name='assessmenttype'), nullable=False),
        sa.Column('version', sa.Integer, server_default='1'),
        sa.Column('total_questions', sa.Integer, server_default='0'),
        sa.Column('time_limit_minutes', sa.Integer, nullable=True),
        sa.Column('is_active', sa.Boolean, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── assessment_questions ──────────────────────────────
    op.create_table('assessment_questions',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('assessment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('assessments.id', ondelete='CASCADE'), nullable=False),
        sa.Column('question_text', sa.Text, nullable=False),
        sa.Column('question_type', sa.String(30), nullable=False),
        sa.Column('category', sa.String(50), nullable=True),
        sa.Column('options', postgresql.JSONB, server_default='[]'),
        sa.Column('order_index', sa.Integer, nullable=False),
        sa.Column('weight', sa.Float, server_default='1.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_assessment_questions_assessment_id', 'assessment_questions', ['assessment_id'])

    # ── assessment_attempts ───────────────────────────────
    op.create_table('assessment_attempts',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('student_profile_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('assessment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('assessments.id'), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('time_taken_seconds', sa.Integer, nullable=True),
        sa.Column('is_complete', sa.Boolean, server_default='false'),
        sa.Column('attempt_number', sa.Integer, server_default='1'),
    )

    # ── assessment_answers ────────────────────────────────
    op.create_table('assessment_answers',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('attempt_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('assessment_attempts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('question_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('assessment_questions.id'), nullable=False),
        sa.Column('selected_option', postgresql.JSONB, nullable=True),
        sa.Column('raw_score', sa.Float, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── assessment_results ────────────────────────────────
    op.create_table('assessment_results',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('attempt_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('assessment_attempts.id'), nullable=False, unique=True),
        sa.Column('student_profile_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('student_profiles.id'), nullable=False),
        sa.Column('assessment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('assessments.id'), nullable=False),
        sa.Column('aptitude_scores', postgresql.JSONB, server_default='{}'),
        sa.Column('interest_scores', postgresql.JSONB, server_default='{}'),
        sa.Column('top_aptitudes', postgresql.JSONB, server_default='[]'),
        sa.Column('top_interests', postgresql.JSONB, server_default='[]'),
        sa.Column('recommended_streams', postgresql.JSONB, server_default='[]'),
        sa.Column('overall_summary', sa.Text, nullable=True),
        sa.Column('computed_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── pathways ──────────────────────────────────────────
    op.create_table('pathways',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('student_profile_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(300), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('status', sa.Enum('DRAFT','GENERATED','SAVED','ARCHIVED', name='pathwaystatus'), server_default='GENERATED'),
        sa.Column('total_duration_years', sa.Float, nullable=True),
        sa.Column('estimated_total_cost', sa.Float, nullable=True),
        sa.Column('cost_currency', sa.String(10), server_default='INR'),
        sa.Column('career_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('careers.id'), nullable=True),
        sa.Column('career_name', sa.String(200), nullable=True),
        sa.Column('compatibility_score', sa.Float, nullable=True),
        sa.Column('interest_fit_score', sa.Float, nullable=True),
        sa.Column('academic_fit_score', sa.Float, nullable=True),
        sa.Column('financial_fit_score', sa.Float, nullable=True),
        sa.Column('constraint_status', sa.String(30), server_default='unknown'),
        sa.Column('hard_constraints_met', sa.Boolean, server_default='true'),
        sa.Column('soft_constraint_issues', postgresql.JSONB, server_default='[]'),
        sa.Column('ai_explanation', sa.Text, nullable=True),
        sa.Column('assumptions', postgresql.JSONB, server_default='[]'),
        sa.Column('uncertainties', postgresql.JSONB, server_default='[]'),
        sa.Column('is_primary', sa.Boolean, server_default='false'),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_pathways_student_profile_id', 'pathways', ['student_profile_id'])

    # ── pathway_steps ─────────────────────────────────────
    op.create_table('pathway_steps',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('pathway_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('pathways.id', ondelete='CASCADE'), nullable=False),
        sa.Column('step_order', sa.Integer, nullable=False),
        sa.Column('step_type', sa.String(50), nullable=False),
        sa.Column('title', sa.String(300), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('institution_name', sa.String(300), nullable=True),
        sa.Column('institution_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('institutions.id'), nullable=True),
        sa.Column('program_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('programs.id'), nullable=True),
        sa.Column('duration_months', sa.Integer, nullable=True),
        sa.Column('cost_estimate', sa.Float, nullable=True),
        sa.Column('cost_currency', sa.String(10), server_default='INR'),
        sa.Column('is_required', sa.Boolean, server_default='true'),
        sa.Column('start_year_offset', sa.Integer, server_default='0'),
        sa.Column('end_year_offset', sa.Integer, nullable=True),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── scenarios ─────────────────────────────────────────
    op.create_table('scenarios',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('student_profile_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('is_base_scenario', sa.Boolean, server_default='false'),
        sa.Column('parent_scenario_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('version', sa.Integer, server_default='1'),
        sa.Column('changes_summary', postgresql.JSONB, server_default='[]'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── notifications ─────────────────────────────────────
    op.create_table('notifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(300), nullable=False),
        sa.Column('message', sa.Text, nullable=False),
        sa.Column('notification_type', sa.String(50), nullable=True),
        sa.Column('is_read', sa.Boolean, server_default='false'),
        sa.Column('read_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('action_url', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_notifications_user_id', 'notifications', ['user_id'])

    # ── saved_items ───────────────────────────────────────
    op.create_table('saved_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('item_type', sa.String(50), nullable=False),
        sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('saved_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── audit_logs ────────────────────────────────────────
    op.create_table('audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('entity_type', sa.String(100), nullable=False),
        sa.Column('entity_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('old_value', postgresql.JSONB, nullable=True),
        sa.Column('new_value', postgresql.JSONB, nullable=True),
        sa.Column('ip_address', sa.String(50), nullable=True),
        sa.Column('user_agent', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_audit_logs_user_id', 'audit_logs', ['user_id'])
    op.create_index('ix_audit_logs_entity_type', 'audit_logs', ['entity_type'])


def downgrade() -> None:
    tables = [
        'audit_logs', 'saved_items', 'notifications', 'pathway_steps', 'pathways',
        'scenarios', 'assessment_results', 'assessment_answers', 'assessment_attempts',
        'assessment_questions', 'assessments', 'loan_products', 'scholarships',
        'programs', 'institutions', 'careers', 'skills', 'industries',
        'work_preferences', 'academic_records', 'student_profiles', 'countries',
        'refresh_tokens', 'users',
    ]
    for table in tables:
        op.drop_table(table)

    for enum in ['pathwaystatus', 'assessmenttype', 'datastatus', 'userrole']:
        op.execute(f'DROP TYPE IF EXISTS {enum}')
    op.execute('DROP EXTENSION IF EXISTS vector')
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')
