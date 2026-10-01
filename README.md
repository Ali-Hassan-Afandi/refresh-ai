# ReFresh AI — GitHub-ready MVP

Cloud-first: Next.js frontend, FastAPI backend, Supabase PostgreSQL, Groq online LLM.
No local AI model is required.

## Runtime
- Python 3.12.11
- Node.js 24.x

## 1. Supabase
Run `supabase/schema.sql` in Supabase SQL Editor.

## 2. Backend local test (Windows PowerShell)
```powershell
cd backend
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Fill the real secrets in backend/.env
python -m uvicorn app.main:app --reload --port 8000
```
Test `/health`, `/database-test`, and `/docs`.

## 3. Frontend local test
```powershell
cd frontend
npm install
Copy-Item .env.local.example .env.local
npm run dev
```

## 4. GitHub
Do NOT commit `.env` or `.env.local`. The root `.gitignore` already excludes them.

## 5. Render backend
Import the GitHub repo and create a Python Web Service:
- Root directory: `backend`
- Build: `pip install -r requirements.txt`
- Start: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health: `/health`
- Set secrets in Render Environment.

`backend/render.yaml` also contains a Blueprint definition.

## 6. Vercel frontend
Import the same repo:
- Root directory: `frontend`
- Framework: Next.js
- Set `NEXT_PUBLIC_API_URL` to the Render service URL.

After Vercel deploys, set Render `FRONTEND_ORIGIN` to the Vercel URL.
