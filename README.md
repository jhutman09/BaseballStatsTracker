# Baseball Stats Tracker

Personal stats tracker for Little League scorebooks. Learning project: React (Vite + Tailwind) frontend, FastAPI backend, PostgreSQL database.

## Backend setup

```
cd backend
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your local Postgres connection string.

Run migrations:
```
.venv\Scripts\alembic upgrade head
```

Run the dev server:
```
.venv\Scripts\uvicorn app.main:app --reload
```

## Frontend

Not built yet.
