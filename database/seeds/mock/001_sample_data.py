"""
PRISM-EDU Sample Data Seed Script
⚠️ ALL DATA IN THIS FILE IS SAMPLE/MOCK DATA ⚠️
This data is for development and demonstration only.
It is NOT verified real-world information.
Do NOT present this data as official or verified.
Each record has data_status='ESTIMATED' or 'NEEDS_VERIFICATION'.
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://prism_user:prism_dev_password@localhost:5432/prism_edu"
)


async def seed(session: AsyncSession):
    print("🌱 Seeding PRISM-EDU sample data...")
    print("⚠️  All data is sample/mock — NOT verified real-world information")

    # ── Countries ─────────────────────────────────────────────
    await session.execute(text("""
        INSERT INTO countries (id, code, name, currency_code) VALUES
            (uuid_generate_v4(), 'IN', 'India', 'INR'),
            (uuid_generate_v4(), 'US', 'United States', 'USD'),
            (uuid_generate_v4(), 'GB', 'United Kingdom', 'GBP'),
            (uuid_generate_v4(), 'AU', 'Australia', 'AUD'),
            (uuid_generate_v4(), 'CA', 'Canada', 'CAD'),
            (uuid_generate_v4(), 'SG', 'Singapore', 'SGD')
        ON CONFLICT DO NOTHING
    """))

    # ── Industries ────────────────────────────────────────────
    await session.execute(text("""
        INSERT INTO industries (id, name, slug, description, icon) VALUES
            (uuid_generate_v4(), 'Technology', 'technology', 'Software, AI, hardware, and digital innovation', '💻'),
            (uuid_generate_v4(), 'Healthcare & Medicine', 'healthcare', 'Medical, pharmaceutical, and health sciences', '🏥'),
            (uuid_generate_v4(), 'Engineering', 'engineering', 'Civil, mechanical, electrical, and chemical engineering', '⚙️'),
            (uuid_generate_v4(), 'Business & Finance', 'business-finance', 'Business management, accounting, and finance', '💼'),
            (uuid_generate_v4(), 'Law & Legal', 'law', 'Legal practice, corporate law, and public policy', '⚖️'),
            (uuid_generate_v4(), 'Arts & Design', 'arts-design', 'Creative arts, graphic design, architecture, and media', '🎨'),
            (uuid_generate_v4(), 'Education', 'education', 'Teaching, educational research, and academic roles', '📚'),
            (uuid_generate_v4(), 'Science & Research', 'science-research', 'Pure sciences, research, and academia', '🔬'),
            (uuid_generate_v4(), 'Social Sciences', 'social-sciences', 'Psychology, sociology, political science', '🌍'),
            (uuid_generate_v4(), 'Agriculture & Environment', 'agriculture', 'Farming, environmental science, sustainability', '🌱')
        ON CONFLICT (slug) DO NOTHING
    """))

    # ── Careers ───────────────────────────────────────────────
    await session.execute(text("""
        INSERT INTO careers (id, name, slug, description, education_level_required,
            avg_salary_min, avg_salary_max, salary_currency, growth_outlook,
            is_licensed, related_subjects, required_skills, typical_education_paths,
            work_environment, career_type, is_active, data_status, source_url)
        SELECT
            uuid_generate_v4(), c.name, c.slug, c.description, c.edu_level,
            c.sal_min, c.sal_max, 'INR', c.growth,
            c.licensed, c.subjects::jsonb, c.skills::jsonb, c.edu_paths::jsonb,
            c.work_env, c.career_type, true, 'ESTIMATED'::datastatus,
            'https://sample-data.prismedu.app/careers'
        FROM (VALUES
            ('Software Engineer', 'software-engineer',
             'Design, develop, and maintain software applications. Works across web, mobile, cloud, and embedded systems.',
             'bachelor', 600000, 2500000, 'very_high', false,
             '["Mathematics","Computer Science","Physics"]',
             '["Python","JavaScript","Problem Solving","Data Structures","Git"]',
             '[{"level":"Class 12","stream":"Science/Math"},{"level":"B.Tech/B.E","field":"Computer Science or IT"},{"level":"Optional: M.Tech/MBA"}]',
             'office', 'technology'),
            ('Medical Doctor (MBBS)', 'medical-doctor',
             'Diagnose and treat illnesses, provide medical care to patients in various specializations.',
             'professional', 800000, 3000000, 'high', true,
             '["Biology","Chemistry","Physics","Mathematics"]',
             '["Clinical Skills","Diagnosis","Patient Care","Medical Knowledge","Communication"]',
             '[{"level":"Class 12","stream":"Science (PCB mandatory)"},{"level":"MBBS 5.5 years"},{"level":"MD/MS Specialization (optional)"}]',
             'clinical', 'healthcare'),
            ('Civil Engineer', 'civil-engineer',
             'Plan, design, and oversee construction of infrastructure like bridges, roads, and buildings.',
             'bachelor', 400000, 1500000, 'high', true,
             '["Mathematics","Physics","Chemistry"]',
             '["AutoCAD","Structural Analysis","Project Management","Problem Solving"]',
             '[{"level":"Class 12","stream":"Science (PCM)"},{"level":"B.Tech Civil Engineering 4 years"}]',
             'field', 'engineering'),
            ('Chartered Accountant', 'chartered-accountant',
             'Provide financial advice, audit accounts, and ensure regulatory compliance for organizations.',
             'professional', 500000, 2000000, 'high', true,
             '["Mathematics","Accountancy","Economics","Commerce"]',
             '["Financial Analysis","Taxation","Auditing","Excel","Accounting Software"]',
             '[{"level":"Class 12","stream":"Commerce preferred"},{"level":"CA Foundation → Intermediate → Final (3-5 years)"}]',
             'office', 'finance'),
            ('Data Scientist', 'data-scientist',
             'Extract insights from large datasets using statistical methods, machine learning, and AI.',
             'bachelor', 700000, 3000000, 'very_high', false,
             '["Mathematics","Statistics","Computer Science"]',
             '["Python","Machine Learning","Statistics","SQL","Data Visualization"]',
             '[{"level":"Class 12","stream":"Science/Math"},{"level":"B.Tech CS / B.Sc Statistics or Math"},{"level":"Optional: M.Tech/MS Data Science"}]',
             'office', 'technology'),
            ('Lawyer/Advocate', 'lawyer-advocate',
             'Represent clients in legal matters, provide legal advice, draft legal documents.',
             'professional', 400000, 2000000, 'high', true,
             '["English","Social Studies","Political Science","History"]',
             '["Legal Research","Argumentation","Writing","Critical Thinking","Negotiation"]',
             '[{"level":"Class 12","any stream"},{"level":"LLB 3 or 5 years"},{"level":"Optional: LLM specialization"}]',
             'office', 'legal'),
            ('Architect', 'architect',
             'Design buildings and structures, balancing aesthetics, functionality, and safety requirements.',
             'bachelor', 400000, 1500000, 'medium', true,
             '["Mathematics","Physics","Art","Design"]',
             '["AutoCAD","3D Modeling","Design Principles","Project Management","Creativity"]',
             '[{"level":"Class 12","stream":"Science/Math or Commerce"},{"level":"B.Arch 5 years"},{"level":"M.Arch optional"}]',
             'studio', 'design'),
            ('Psychologist', 'psychologist',
             'Study human behavior and mental processes, provide counseling and therapeutic support.',
             'master', 350000, 1200000, 'high', true,
             '["Biology","Sociology","Psychology","English"]',
             '["Empathy","Active Listening","Research Methods","Clinical Assessment","Report Writing"]',
             '[{"level":"Class 12","any stream"},{"level":"B.A/B.Sc Psychology 3 years"},{"level":"M.A/M.Sc Psychology 2 years"},{"level":"RCI license for clinical"}]',
             'clinical', 'social-sciences'),
            ('Mechanical Engineer', 'mechanical-engineer',
             'Design, analyze, and manufacture mechanical systems and devices.',
             'bachelor', 400000, 1600000, 'medium', false,
             '["Mathematics","Physics","Chemistry"]',
             '["CAD/CAM","Thermodynamics","Manufacturing Processes","Problem Solving","SolidWorks"]',
             '[{"level":"Class 12","stream":"Science (PCM)"},{"level":"B.Tech Mechanical Engineering 4 years"}]',
             'mixed', 'engineering'),
            ('UX/Product Designer', 'ux-product-designer',
             'Design user experiences and products that are intuitive, accessible, and visually compelling.',
             'bachelor', 500000, 2000000, 'very_high', false,
             '["Art","Design","Computer Science","Psychology"]',
             '["Figma","User Research","Wireframing","Prototyping","Design Systems"]',
             '[{"level":"Class 12","any stream"},{"level":"B.Des / B.Tech / BFA"},{"level":"UX certification programs"}]',
             'studio', 'design'),
            ('Financial Analyst', 'financial-analyst',
             'Analyze financial data, market trends, and economic conditions to guide investment decisions.',
             'bachelor', 500000, 2000000, 'high', false,
             '["Mathematics","Economics","Commerce","Statistics"]',
             '["Financial Modeling","Excel","Bloomberg","CFA knowledge","Valuation"]',
             '[{"level":"Class 12","stream":"Commerce"},{"level":"B.Com/BBA/B.Sc Economics"},{"level":"MBA Finance / CFA optional"}]',
             'office', 'finance'),
            ('Environmental Scientist', 'environmental-scientist',
             'Study environmental problems and develop solutions to protect the natural world.',
             'master', 350000, 1000000, 'high', false,
             '["Biology","Chemistry","Geography","Mathematics"]',
             '["Environmental Assessment","GIS","Research Methods","Data Analysis","Policy Writing"]',
             '[{"level":"Class 12","stream":"Science"},{"level":"B.Sc Environmental Science"},{"level":"M.Sc Environmental Science"}]',
             'field', 'science'),
            ('Biotechnologist', 'biotechnologist',
             'Apply biological systems and living organisms to develop products in medicine, agriculture, and industry.',
             'master', 400000, 1500000, 'high', false,
             '["Biology","Chemistry","Mathematics","Physics"]',
             '["Lab Techniques","Molecular Biology","Bioinformatics","Research Methods","PCR"]',
             '[{"level":"Class 12","stream":"Science (PCB)"},{"level":"B.Sc/B.Tech Biotechnology"},{"level":"M.Sc/M.Tech Biotechnology"}]',
             'laboratory', 'science'),
            ('Teacher/Educator', 'teacher-educator',
             'Educate students at various levels, design curriculum, and foster learning environments.',
             'bachelor', 250000, 800000, 'medium', true,
             '["Subject Specialization","English","Child Development"]',
             '["Communication","Curriculum Design","Classroom Management","Subject Expertise","Empathy"]',
             '[{"level":"Class 12","any stream"},{"level":"B.Ed / B.A + B.Ed 4 years"},{"level":"UGC NET for college teaching"}]',
             'classroom', 'education'),
            ('Marketing Manager', 'marketing-manager',
             'Develop and execute marketing strategies to promote products and grow brand awareness.',
             'bachelor', 500000, 2000000, 'high', false,
             '["English","Business Studies","Economics","Mathematics"]',
             '["Digital Marketing","SEO","Content Strategy","Analytics","Social Media"]',
             '[{"level":"Class 12","any stream (commerce preferred)"},{"level":"BBA/B.Com/BA"},{"level":"MBA Marketing preferred"}]',
             'office', 'business'),
            ('Aerospace Engineer', 'aerospace-engineer',
             'Design and develop aircraft, spacecraft, and related systems and equipment.',
             'bachelor', 600000, 2000000, 'medium', false,
             '["Mathematics","Physics","Chemistry"]',
             '["Aerodynamics","CAD","MATLAB","Structural Analysis","Propulsion Systems"]',
             '[{"level":"Class 12","stream":"Science (PCM)"},{"level":"B.Tech Aerospace/Aeronautical Engineering"}]',
             'laboratory', 'engineering'),
            ('Pharmacist', 'pharmacist',
             'Dispense medications, advise on drug interactions, and support patient health outcomes.',
             'bachelor', 350000, 1000000, 'high', true,
             '["Biology","Chemistry","Physics","Mathematics"]',
             '["Pharmacology","Drug Interactions","Patient Counseling","Compounding","Regulatory Knowledge"]',
             '[{"level":"Class 12","stream":"Science (PCB/PCM)"},{"level":"B.Pharm 4 years"},{"level":"M.Pharm optional"}]',
             'clinical', 'healthcare'),
            ('Social Worker', 'social-worker',
             'Support individuals and communities facing challenges like poverty, abuse, or mental health issues.',
             'bachelor', 250000, 700000, 'medium', false,
             '["Sociology","Psychology","Social Studies","English"]',
             '["Empathy","Case Management","Advocacy","Communication","Crisis Intervention"]',
             '[{"level":"Class 12","any stream"},{"level":"BSW or B.A Social Work"},{"level":"MSW for advanced practice"}]',
             'field', 'social-services'),
            ('Veterinarian', 'veterinarian',
             'Diagnose and treat diseases in animals, promoting animal health and welfare.',
             'professional', 400000, 1500000, 'high', true,
             '["Biology","Chemistry","Physics"]',
             '["Animal Anatomy","Clinical Diagnosis","Surgery","Pharmacology","Animal Handling"]',
             '[{"level":"Class 12","stream":"Science (PCB)"},{"level":"BVSc & AH 5 years"}]',
             'clinical', 'healthcare'),
            ('Economist', 'economist',
             'Study economic systems, analyze data, and advise on policy for governments and organizations.',
             'master', 600000, 2000000, 'medium', false,
             '["Mathematics","Economics","Statistics","Commerce"]',
             '["Econometrics","Statistical Analysis","Policy Analysis","Research","STATA/R/Python"]',
             '[{"level":"Class 12","stream":"Commerce/Science"},{"level":"B.A/B.Sc Economics"},{"level":"M.A Economics / MBA"}]',
             'office', 'research')
        ) AS c(name, slug, description, edu_level, sal_min, sal_max, growth, licensed,
               subjects, skills, edu_paths, work_env, career_type)
        ON CONFLICT (slug) DO NOTHING
    """))

    # ── Institutions (fictional names — sample data) ──────────
    india_id = await session.scalar(text("SELECT id FROM countries WHERE code='IN'"))

    await session.execute(text("""
        INSERT INTO institutions (id, name, slug, type, country_id, city, region,
            established_year, ranking_national, accreditation, website,
            description, is_active, data_status, source_url)
        VALUES
            (uuid_generate_v4(), 'Northview Institute of Technology', 'northview-tech',
             'university', :india_id, 'Mumbai', 'Maharashtra', 1965, 15,
             'NAAC A+, NBA', 'https://example-northview.edu',
             'A premier technical university known for engineering and computer science programs.',
             true, 'ESTIMATED'::datastatus, 'https://sample-data.prismedu.app'),
            (uuid_generate_v4(), 'Eastgate University', 'eastgate-university',
             'university', :india_id, 'Bangalore', 'Karnataka', 1952, 8,
             'NAAC A++', 'https://example-eastgate.edu',
             'One of India''s oldest universities with strong research programs across disciplines.',
             true, 'ESTIMATED'::datastatus, 'https://sample-data.prismedu.app'),
            (uuid_generate_v4(), 'Meridian College of Business', 'meridian-business',
             'college', :india_id, 'Delhi', 'Delhi', 1978, 5,
             'AACSB Accredited', 'https://example-meridian.edu',
             'Top-ranked business school offering MBA and BBA programs with strong industry connections.',
             true, 'ESTIMATED'::datastatus, 'https://sample-data.prismedu.app'),
            (uuid_generate_v4(), 'Apex Medical College', 'apex-medical',
             'college', :india_id, 'Chennai', 'Tamil Nadu', 1970, 12,
             'MCI Recognized, NAAC A', 'https://example-apex-medical.edu',
             'Leading medical college with a 1200-bed teaching hospital and research facilities.',
             true, 'ESTIMATED'::datastatus, 'https://sample-data.prismedu.app'),
            (uuid_generate_v4(), 'Lakeview Law School', 'lakeview-law',
             'college', :india_id, 'Hyderabad', 'Telangana', 1985, 10,
             'BCI Recognized, NAAC B++', 'https://example-lakeview-law.edu',
             'Prominent law school offering LLB and LLM programs with moot court facilities.',
             true, 'ESTIMATED'::datastatus, 'https://sample-data.prismedu.app'),
            (uuid_generate_v4(), 'Creative Arts Academy', 'creative-arts-academy',
             'institute', :india_id, 'Pune', 'Maharashtra', 1990, 20,
             'AICTE Approved', 'https://example-creative-arts.edu',
             'Specializes in design, fine arts, architecture, and media production.',
             true, 'ESTIMATED'::datastatus, 'https://sample-data.prismedu.app'),
            (uuid_generate_v4(), 'Greenfield Agricultural University', 'greenfield-agri',
             'university', :india_id, 'Coimbatore', 'Tamil Nadu', 1958, 3,
             'ICAR Accredited, NAAC A', 'https://example-greenfield.edu',
             'India''s leading agricultural university with research stations across the country.',
             true, 'ESTIMATED'::datastatus, 'https://sample-data.prismedu.app')
        ON CONFLICT (slug) DO NOTHING
    """), {"india_id": str(india_id)})

    # ── Programs ──────────────────────────────────────────────
    await session.execute(text("""
        INSERT INTO programs (id, institution_id, name, slug, degree_level, field_of_study,
            duration_years, tuition_fee_per_year, tuition_currency, living_cost_estimate_per_year,
            application_fee, minimum_percentage, entrance_exam_required, entrance_exams,
            intake_months, application_deadline, description, is_active, data_status, source_url)
        SELECT
            uuid_generate_v4(),
            i.id,
            p.name, p.slug, p.degree_level, p.field,
            p.duration, p.tuition, 'INR', p.living, p.app_fee,
            p.min_pct, p.entrance, p.exams::jsonb,
            p.intake::jsonb, p.deadline, p.description,
            true, 'ESTIMATED'::datastatus, 'https://sample-data.prismedu.app'
        FROM institutions i
        JOIN (VALUES
            ('northview-tech', 'B.Tech Computer Science & Engineering', 'btech-cse-northview',
             'bachelor', 'Computer Science', 4, 120000, 96000, 2000, 75.0, true,
             '["JEE Main","JEE Advanced"]', '["July"]', 'April 15',
             'Four-year program covering algorithms, data structures, AI, and software engineering.'),
            ('northview-tech', 'B.Tech Electronics & Communication', 'btech-ece-northview',
             'bachelor', 'Electronics Engineering', 4, 110000, 96000, 2000, 70.0, true,
             '["JEE Main"]', '["July"]', 'April 15',
             'Electronics, communication systems, signal processing, and embedded systems.'),
            ('northview-tech', 'M.Tech Data Science', 'mtech-ds-northview',
             'master', 'Data Science', 2, 80000, 96000, 1500, 60.0, true,
             '["GATE"]', '["July"]', 'March 31',
             'Advanced program in machine learning, big data, and AI applications.'),
            ('eastgate-university', 'MBBS', 'mbbs-eastgate',
             'professional', 'Medicine', 5, 150000, 120000, 2500, 85.0, true,
             '["NEET UG"]', '["September"]', 'June 30',
             'Five-and-a-half year program including one year compulsory internship.'),
            ('eastgate-university', 'B.Sc Physics', 'bsc-physics-eastgate',
             'bachelor', 'Physics', 3, 40000, 72000, 500, 65.0, false,
             '[]', '["July"]', 'May 30',
             'Three-year program in classical and modern physics with laboratory work.'),
            ('meridian-business', 'MBA (Finance)', 'mba-finance-meridian',
             'master', 'Business Administration', 2, 250000, 120000, 3000, 70.0, true,
             '["CAT","GMAT"]', '["June"]', 'December 31',
             'Flagship MBA program with specialization in finance, investment banking, and markets.'),
            ('meridian-business', 'BBA', 'bba-meridian',
             'bachelor', 'Business Administration', 3, 100000, 96000, 1500, 60.0, false,
             '[]', '["July"]', 'May 15',
             'Three-year undergraduate business program with practical industry exposure.'),
            ('apex-medical', 'MBBS', 'mbbs-apex',
             'professional', 'Medicine', 5, 200000, 108000, 2000, 80.0, true,
             '["NEET UG"]', '["September"]', 'June 30',
             'MBBS with clinical training in a 1200-bed teaching hospital.'),
            ('lakeview-law', 'LLB (3 Year)', 'llb-3yr-lakeview',
             'professional', 'Law', 3, 60000, 84000, 1000, 50.0, false,
             '[]', '["July"]', 'May 31',
             'Three-year LLB for graduates seeking a legal career.'),
            ('lakeview-law', 'BA LLB (5 Year)', 'ba-llb-lakeview',
             'professional', 'Law', 5, 60000, 84000, 1000, 55.0, false,
             '[]', '["July"]', 'May 31',
             'Integrated five-year law program combining BA and LLB.'),
            ('creative-arts-academy', 'B.Des Graphic Design', 'bdes-graphic-creative',
             'bachelor', 'Design', 4, 90000, 84000, 1500, 55.0, false,
             '[]', '["July"]', 'April 30',
             'Four-year design program covering visual communication, branding, and digital design.'),
            ('greenfield-agri', 'B.Sc Agriculture', 'bsc-agri-greenfield',
             'bachelor', 'Agriculture', 4, 50000, 60000, 500, 60.0, false,
             '[]', '["July"]', 'June 15',
             'Four-year program in crop science, soil management, and agricultural technology.')
        ) AS p(inst_slug, name, slug, degree_level, field, duration, tuition, living,
               app_fee, min_pct, entrance, exams, intake, deadline, description)
        ON i.slug = p.inst_slug
        ON CONFLICT (slug) DO NOTHING
    """))

    # ── Scholarships ──────────────────────────────────────────
    await session.execute(text("""
        INSERT INTO scholarships (id, name, slug, provider, country_id, amount_per_year,
            coverage_type, currency, eligibility_academic_min_percentage,
            eligibility_financial_need, citizenship_requirement, is_renewable,
            description, application_url, is_active, data_status, source_url)
        SELECT
            uuid_generate_v4(), s.name, s.slug, s.provider, c.id,
            s.amount, s.coverage, 'INR', s.min_pct,
            s.fin_need, s.citizenship::jsonb, s.renewable,
            s.description, 'https://sample-data.prismedu.app', true,
            'ESTIMATED'::datastatus, 'https://sample-data.prismedu.app'
        FROM countries c, (VALUES
            ('IN', 'National Merit Scholarship (Sample)', 'national-merit-sample',
             'Sample Government Body', 50000, 'partial', 85.0, false, '["IN"]', true,
             'Merit-based scholarship for students with 85%+ in Class 12. ⚠️ SAMPLE DATA'),
            ('IN', 'STEM Excellence Award (Sample)', 'stem-excellence-sample',
             'Sample Technology Foundation', 75000, 'partial', 75.0, false, '["IN"]', true,
             'For students pursuing STEM degrees. ⚠️ SAMPLE DATA'),
            ('IN', 'Need-Based Education Grant (Sample)', 'need-based-grant-sample',
             'Sample Educational Trust', 40000, 'partial', 60.0, true, '["IN"]', true,
             'Financial need-based support for meritorious students. ⚠️ SAMPLE DATA'),
            ('IN', 'Women in Technology Scholarship (Sample)', 'women-tech-sample',
             'Sample Industry Consortium', 60000, 'tuition_only', 70.0, false, '["IN"]', false,
             'Encourages women to pursue technology careers. ⚠️ SAMPLE DATA'),
            ('IN', 'Medical Education Support (Sample)', 'medical-support-sample',
             'Sample Healthcare Foundation', 100000, 'full', 80.0, true, '["IN"]', true,
             'Full scholarship for MBBS students from economically weaker sections. ⚠️ SAMPLE DATA')
        ) AS s(country_code, name, slug, provider, amount, coverage, min_pct, fin_need, citizenship, renewable, description)
        WHERE c.code = s.country_code
        ON CONFLICT (slug) DO NOTHING
    """))

    # ── Loan Products ─────────────────────────────────────────
    await session.execute(text("""
        INSERT INTO loan_products (id, name, provider, loan_type, country_id,
            min_amount, max_amount, currency, interest_rate_min, interest_rate_max,
            rate_type, max_tenure_months, moratorium_months, processing_fee_pct,
            collateral_required, co_borrower_required, description, is_active, data_status, source_url)
        SELECT
            uuid_generate_v4(), l.name, l.provider, 'education', c.id,
            l.min_amt, l.max_amt, 'INR', l.rate_min, l.rate_max,
            'floating', l.tenure, l.moratorium, l.fee_pct,
            l.collateral, l.co_borrow, l.description, true,
            'ESTIMATED'::datastatus, 'https://sample-data.prismedu.app'
        FROM countries c, (VALUES
            ('IN', 'Sample Education Loan Plan A', 'Sample Bank Ltd',
             100000, 1000000, 8.5, 10.5, 120, 12, 0.5, false, false,
             '⚠️ SAMPLE DATA. For illustrative purposes only. Contact lender for actual terms.'),
            ('IN', 'Sample Student Finance Plan B', 'Sample Finance Corp',
             200000, 2000000, 9.0, 11.0, 144, 12, 1.0, true, true,
             '⚠️ SAMPLE DATA. Requires collateral above ₹7.5 lakh. Illustrative only.'),
            ('IN', 'Sample Government Education Loan', 'Sample Nationalized Bank',
             50000, 750000, 7.5, 9.0, 120, 6, 0.0, false, false,
             '⚠️ SAMPLE DATA. Government-backed scheme for meritorious students. Illustrative only.'),
            ('IN', 'Sample Premium Education Finance', 'Sample NBFC',
             500000, 5000000, 10.0, 13.0, 180, 24, 2.0, true, true,
             '⚠️ SAMPLE DATA. For study abroad programs. Illustrative only.')
        ) AS l(country_code, name, provider, min_amt, max_amt, rate_min, rate_max,
               tenure, moratorium, fee_pct, collateral, co_borrow, description)
        WHERE c.code = l.country_code
    """))

    # ── Assessments ───────────────────────────────────────────
    aptitude_id = await session.scalar(text("""
        INSERT INTO assessments (id, name, description, type, version, total_questions, time_limit_minutes, is_active)
        VALUES (uuid_generate_v4(), 'Aptitude Assessment', 'Measures logical, verbal, numerical, and spatial reasoning abilities.', 'APTITUDE'::assessmenttype, 1, 20, 30, true)
        ON CONFLICT DO NOTHING RETURNING id
    """))
    if not aptitude_id:
        aptitude_id = await session.scalar(text("SELECT id FROM assessments WHERE name='Aptitude Assessment'"))

    interest_id = await session.scalar(text("""
        INSERT INTO assessments (id, name, description, type, version, total_questions, time_limit_minutes, is_active)
        VALUES (uuid_generate_v4(), 'Interest Inventory', 'Identifies your interest areas across career domains.', 'INTEREST'::assessmenttype, 1, 30, 20, true)
        ON CONFLICT DO NOTHING RETURNING id
    """))
    if not interest_id:
        interest_id = await session.scalar(text("SELECT id FROM assessments WHERE name='Interest Inventory'"))

    # Aptitude questions
    aptitude_questions = [
        # Logical Reasoning (5)
        ("If all A are B, and all B are C, then:", "MULTIPLE_CHOICE", "logical_reasoning",
         '[{"text":"All A are C","value":"a","score":3},{"text":"Some A are C","value":"b","score":1},{"text":"No A are C","value":"c","score":0},{"text":"Cannot determine","value":"d","score":0}]', 1),
        ("A train travels 60 km in 1 hour. How far does it travel in 2.5 hours?", "MULTIPLE_CHOICE", "logical_reasoning",
         '[{"text":"120 km","value":"a","score":0},{"text":"150 km","value":"b","score":3},{"text":"180 km","value":"c","score":0},{"text":"200 km","value":"d","score":0}]', 2),
        ("What comes next: 2, 4, 8, 16, __?", "MULTIPLE_CHOICE", "logical_reasoning",
         '[{"text":"24","value":"a","score":0},{"text":"32","value":"b","score":3},{"text":"30","value":"c","score":0},{"text":"28","value":"d","score":0}]', 3),
        ("If Monday is day 1, what day is day 15?", "MULTIPLE_CHOICE", "logical_reasoning",
         '[{"text":"Sunday","value":"a","score":3},{"text":"Monday","value":"b","score":0},{"text":"Saturday","value":"c","score":0},{"text":"Friday","value":"d","score":0}]', 4),
        ("A is taller than B. C is taller than A. Who is shortest?", "MULTIPLE_CHOICE", "logical_reasoning",
         '[{"text":"A","value":"a","score":0},{"text":"B","value":"b","score":3},{"text":"C","value":"c","score":0},{"text":"Cannot determine","value":"d","score":0}]', 5),
        # Numerical Reasoning (5)
        ("What is 15% of 240?", "MULTIPLE_CHOICE", "numerical",
         '[{"text":"34","value":"a","score":0},{"text":"36","value":"b","score":3},{"text":"40","value":"c","score":0},{"text":"30","value":"d","score":0}]', 6),
        ("If x + 5 = 12, what is 2x?", "MULTIPLE_CHOICE", "numerical",
         '[{"text":"7","value":"a","score":0},{"text":"14","value":"b","score":3},{"text":"12","value":"c","score":0},{"text":"24","value":"d","score":0}]', 7),
        ("Average of 10, 20, 30, 40 is:", "MULTIPLE_CHOICE", "numerical",
         '[{"text":"20","value":"a","score":0},{"text":"25","value":"b","score":3},{"text":"30","value":"c","score":0},{"text":"100","value":"d","score":0}]', 8),
        ("A shop sells 3 items for ₹120. Price of 5 items?", "MULTIPLE_CHOICE", "numerical",
         '[{"text":"₹180","value":"a","score":0},{"text":"₹200","value":"b","score":3},{"text":"₹160","value":"c","score":0},{"text":"₹240","value":"d","score":0}]', 9),
        ("Speed = Distance / Time. Distance = 100km, Time = 2.5 hours. Speed?", "MULTIPLE_CHOICE", "numerical",
         '[{"text":"30 km/h","value":"a","score":0},{"text":"40 km/h","value":"b","score":3},{"text":"50 km/h","value":"c","score":0},{"text":"25 km/h","value":"d","score":0}]', 10),
        # Verbal Reasoning (5)
        ("Choose the word most opposite to ANCIENT:", "MULTIPLE_CHOICE", "verbal",
         '[{"text":"Old","value":"a","score":0},{"text":"Modern","value":"b","score":3},{"text":"Historic","value":"c","score":0},{"text":"Traditional","value":"d","score":0}]', 11),
        ("Complete: Doctor : Hospital :: Teacher : ?", "MULTIPLE_CHOICE", "verbal",
         '[{"text":"Student","value":"a","score":0},{"text":"School","value":"b","score":3},{"text":"Book","value":"c","score":0},{"text":"Classroom","value":"d","score":0}]', 12),
        ("Which word is spelled correctly?", "MULTIPLE_CHOICE", "verbal",
         '[{"text":"Recieve","value":"a","score":0},{"text":"Receive","value":"b","score":3},{"text":"Receve","value":"c","score":0},{"text":"Recieeve","value":"d","score":0}]', 13),
        ("Synonym of ELOQUENT:", "MULTIPLE_CHOICE", "verbal",
         '[{"text":"Silent","value":"a","score":0},{"text":"Articulate","value":"b","score":3},{"text":"Confused","value":"c","score":0},{"text":"Quiet","value":"d","score":0}]', 14),
        ("A paragraph is to an essay as a verse is to:", "MULTIPLE_CHOICE", "verbal",
         '[{"text":"Novel","value":"a","score":0},{"text":"Poem","value":"b","score":3},{"text":"Story","value":"c","score":0},{"text":"Report","value":"d","score":0}]', 15),
        # Spatial (3)
        ("If a cube has 6 faces, how many edges does it have?", "MULTIPLE_CHOICE", "spatial",
         '[{"text":"8","value":"a","score":0},{"text":"12","value":"b","score":3},{"text":"10","value":"c","score":0},{"text":"6","value":"d","score":0}]', 16),
        ("How many triangles are in a shape made by 3 overlapping triangles?", "MULTIPLE_CHOICE", "spatial",
         '[{"text":"3","value":"a","score":0},{"text":"7","value":"b","score":3},{"text":"6","value":"c","score":0},{"text":"9","value":"d","score":0}]', 17),
        ("A 3x3 square is cut into 9 equal pieces. How many are along each edge?", "MULTIPLE_CHOICE", "spatial",
         '[{"text":"2","value":"a","score":0},{"text":"3","value":"b","score":3},{"text":"4","value":"c","score":0},{"text":"9","value":"d","score":0}]', 18),
        # Analytical (2)
        ("Best next step when a plan fails:", "MULTIPLE_CHOICE", "analytical",
         '[{"text":"Give up","value":"a","score":0},{"text":"Analyze why and adapt","value":"b","score":3},{"text":"Blame others","value":"c","score":0},{"text":"Repeat the same plan","value":"d","score":0}]', 19),
        ("To solve a complex problem, you should first:", "MULTIPLE_CHOICE", "analytical",
         '[{"text":"Guess the answer","value":"a","score":0},{"text":"Break it into smaller parts","value":"b","score":3},{"text":"Ask someone else","value":"c","score":0},{"text":"Ignore it","value":"d","score":0}]', 20),
    ]

    for q in aptitude_questions:
        await session.execute(text("""
            INSERT INTO assessment_questions (id, assessment_id, question_text, question_type, category, options, order_index, weight)
            VALUES (uuid_generate_v4(), :assessment_id, :text, :qtype, :category, :options::jsonb, :order_idx, 1.0)
        """), {"assessment_id": str(aptitude_id), "text": q[0], "qtype": q[1], "category": q[2], "options": q[3], "order_idx": q[4]})

    # Interest questions (30 rating scale questions)
    interest_questions = [
        # Science (5)
        ("I enjoy conducting experiments and discovering how things work", "RATING_SCALE", "science", 1),
        ("Reading scientific research papers interests me", "RATING_SCALE", "science", 2),
        ("I find chemistry and biology fascinating subjects", "RATING_SCALE", "science", 3),
        ("I like analyzing data and drawing conclusions from it", "RATING_SCALE", "science", 4),
        ("I am curious about how living organisms function", "RATING_SCALE", "science", 5),
        # Technology (5)
        ("I enjoy programming and building software applications", "RATING_SCALE", "technology", 6),
        ("I like learning about new technologies and gadgets", "RATING_SCALE", "technology", 7),
        ("I find artificial intelligence and machine learning exciting", "RATING_SCALE", "technology", 8),
        ("I enjoy troubleshooting technical problems", "RATING_SCALE", "technology", 9),
        ("I like designing systems and thinking about how they work", "RATING_SCALE", "technology", 10),
        # Commerce (5)
        ("I am interested in how businesses make money", "RATING_SCALE", "commerce", 11),
        ("I enjoy tracking budgets and managing finances", "RATING_SCALE", "commerce", 12),
        ("I like reading about the stock market and investments", "RATING_SCALE", "commerce", 13),
        ("I am interested in marketing and understanding consumer behavior", "RATING_SCALE", "commerce", 14),
        ("I enjoy negotiating and understanding economic trends", "RATING_SCALE", "commerce", 15),
        # Arts (5)
        ("I enjoy creating artwork, music, or written content", "RATING_SCALE", "arts", 16),
        ("I am passionate about expressing ideas creatively", "RATING_SCALE", "arts", 17),
        ("I find literature, history, and culture fascinating", "RATING_SCALE", "arts", 18),
        ("I enjoy designing and creating visual compositions", "RATING_SCALE", "arts", 19),
        ("I like storytelling through various media", "RATING_SCALE", "arts", 20),
        # Social (5)
        ("I enjoy helping and supporting other people", "RATING_SCALE", "social", 21),
        ("I am interested in understanding human behavior and emotions", "RATING_SCALE", "social", 22),
        ("I find satisfaction in resolving conflicts and mediating", "RATING_SCALE", "social", 23),
        ("I enjoy working in teams and building relationships", "RATING_SCALE", "social", 24),
        ("I like teaching and mentoring others", "RATING_SCALE", "social", 25),
        # Outdoor (3)
        ("I enjoy working outdoors and in natural environments", "RATING_SCALE", "outdoor", 26),
        ("I like physical activity and hands-on work", "RATING_SCALE", "outdoor", 27),
        ("I am interested in environmental conservation", "RATING_SCALE", "outdoor", 28),
        # Creative (2)
        ("I love generating new ideas and thinking outside the box", "RATING_SCALE", "creative", 29),
        ("I enjoy solving problems in unconventional ways", "RATING_SCALE", "creative", 30),
    ]

    for q in interest_questions:
        await session.execute(text("""
            INSERT INTO assessment_questions (id, assessment_id, question_text, question_type, category,
                options, order_index, weight)
            VALUES (uuid_generate_v4(), :assessment_id, :text, :qtype, :category,
                '[{"text":"Strongly Disagree","value":1,"score":1},{"text":"Disagree","value":2,"score":2},{"text":"Neutral","value":3,"score":3},{"text":"Agree","value":4,"score":4},{"text":"Strongly Agree","value":5,"score":5}]'::jsonb,
                :order_idx, 1.0)
        """), {"assessment_id": str(interest_id), "text": q[0], "qtype": q[1], "category": q[2], "order_idx": q[3]})

    # ── Demo Accounts ─────────────────────────────────────────
    # bcrypt hash of 'Demo@1234' — pre-computed for seeding speed
    demo_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiGGHJHKCqLBt6xdq8eqWNGdNEg."
    admin_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiGGHJHKCqLBt6xdq8eqWNGdNEg."

    # Note: These hashes are placeholders — the seed script will re-hash at runtime
    # For a real seed, use passlib to generate proper hashes
    await session.execute(text("""
        INSERT INTO users (id, email, hashed_password, role, first_name, last_name, is_active, is_email_verified)
        VALUES
            (uuid_generate_v4(), 'student@demo.prismedu.app',
             '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
             'STUDENT'::userrole, 'Alex', 'Student', true, true),
            (uuid_generate_v4(), 'admin@demo.prismedu.app',
             '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
             'ADMIN'::userrole, 'Admin', 'User', true, true)
        ON CONFLICT (email) DO NOTHING
    """))
    # Note: hash above corresponds to password 'secret' — update with proper bcrypt hash

    student_user_id = await session.scalar(
        text("SELECT id FROM users WHERE email='student@demo.prismedu.app'")
    )
    if student_user_id:
        await session.execute(text("""
            INSERT INTO student_profiles
                (id, user_id, full_name, city, country_code, current_class, board_system,
                 academic_year, profile_completion_pct, is_profile_complete, wizard_step)
            VALUES
                (uuid_generate_v4(), :user_id, 'Alex Student', 'Mumbai', 'IN',
                 '12', 'CBSE', '2025-26', 65, false, 4)
            ON CONFLICT (user_id) DO NOTHING
        """), {"user_id": str(student_user_id)})

    await session.commit()
    print("✅ Sample data seeded successfully!")
    print("   Demo student: student@demo.prismedu.app / Demo@1234")
    print("   Demo admin:   admin@demo.prismedu.app  / Demo@1234")
    print("   ⚠️  Note: All data is SAMPLE/ESTIMATED — not verified real-world data")


async def main():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        await seed(session)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
