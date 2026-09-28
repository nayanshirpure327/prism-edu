# PRISM-EDU

PRISM-EDU is an AI-powered career and education guidance platform designed to help students explore careers, compare institutions, evaluate pathways, and understand funding and scholarship options.

## Project overview

The app combines:

- a Next.js + TypeScript frontend for the student experience
- a FastAPI backend for authentication, APIs, and data processing
- seeded demo data for local testing and onboarding
- educational and career decision tools such as pathways, scholarships, loans, and scenario analysis

## Tech stack

- Frontend: Next.js 14, React, TypeScript, Tailwind CSS
- Backend: FastAPI, Python
- Database: SQLite for local development and seeded mock data
- Authentication: JWT-based login flow
- Testing: pytest and frontend build validation

## Repository structure

```text
prism-edu/
├── apps/
│   ├── api/
│   │   ├── alembic/
│   │   ├── app/
│   │   │   ├── core/
│   │   │   ├── domains/
│   │   │   ├── models/
│   │   │   └── main.py
│   │   ├── database/
│   │   ├── keys/
│   │   ├── scripts/
│   │   ├── Dockerfile
│   │   ├── alembic.ini
│   │   ├── generate.py
│   │   ├── requirements.txt
│   │   └── requirements-dev.txt
│   └── web/
│       ├── app/
│       ├── components/
│       ├── hooks/
│       ├── lib/
│       ├── public/
│       ├── Dockerfile
│       ├── next.config.js
│       ├── package.json
│       ├── postcss.config.js
│       ├── tailwind.config.ts
│       └── tsconfig.json
├── database/
│   └── seeds/
│       └── mock/
├── docs/
├── infrastructure/
│   └── ci/
├── packages/
├── scripts/
├── services/
│   └── workers/
├── tests/
│   ├── e2e/
│   ├── integration/
│   └── unit/
├── docker-compose.yml
├── docker-compose.test.yml
├── README.md
├── .gitignore
└── .env.example (if present in your setup)
```

## Backend structure

The backend lives in `apps/api` and contains:

- `app/main.py` — FastAPI app bootstrap and route registration
- `app/core/` — configuration, database, Redis, security, and exceptions
- `app/domains/` — feature modules such as auth, career, scholarships, assessments, pathways, finance, reports, and institutions
- `app/models/` — data models for the application
- `database/seeds/mock/` — seeded local mock data for testing

## Frontend structure

The frontend lives in `apps/web` and contains:

- `app/` — page routes, auth screens, dashboard, and app shell
- `components/` — reusable UI components and layout sections
- `hooks/` — data-fetching hooks for careers, pathways, institutions, loans, etc.
- `lib/` — API client, auth helpers, utility functions, and shared types
- `public/` — static assets and branding files

## Local setup

### Prerequisites

- Node.js 20+
- Python 3.12+
- npm
- Git
- A terminal (PowerShell or bash)

### 1) Install backend dependencies

```bash
cd apps/api
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Start the API:

```bash
uvicorn app.main:app --reload --port 8000
```

API URLs:

- http://localhost:8000
- Swagger docs: http://localhost:8000/docs

### 2) Install frontend dependencies

Open a new terminal and run:

```bash
cd apps/web
npm install
npm run dev
```

Frontend URLs:

- http://localhost:3000
- If port 3000 is busy, Next.js may run on http://localhost:3001

## Demo login credentials

The project includes a seeded demo account for testing the user flows locally.

- Email: `student@demo.prismedu.app`
- Password: `Demo@1234`

Use those credentials on the login page to access the app dashboard and demo experience.

## Typical run flow

1. Start the backend from `apps/api`
2. Start the frontend from `apps/web`
3. Open the frontend URL in the browser
4. Sign in with the demo account above
5. Explore the dashboard, careers, pathways, institutions, scholarships, and scenario tools

## Useful commands

### Backend

```bash
cd apps/api
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd apps/web
npm install
npm run dev
npm run build
```

### Tests

```bash
cd apps/api
pytest
```

## Notes

- This repo is configured with mock seed data for local use and demos.
- The default demo account is intentionally simple for testing and onboarding.
- For production, use secure environment variables and real deployment configuration for database, secrets, and auth.

## License

This project is intended for local development and demonstration use unless otherwise specified by the repository owner.

