# 🚀 ATD-System: Standalone Attendance Tracker

[![Next.js](https://img.shields.io/badge/Next.js-16-blue?style=flat&logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-yellow?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-green?style=flat&logo=postgresql)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?style=flat&logo=docker)](https://docker.com)
[![Vercel](https://img.shields.io/badge/Vercel-Deploy-orange?style=flat&logo=vercel)](https://vercel.com)

A modern, full-stack **attendance tracking system** for clocking in/out with history. Built with **Next.js 16 (App Router)** frontend, **FastAPI** backend, **PostgreSQL** database. Runs locally via Docker or deploys free on **Vercel + Supabase**.

## ✨ Features
- Clock In/Out with timestamps
- Recent attendance history
- Responsive UI (globe/world animations)
- Local dev (Docker Compose) or serverless prod
- Zero-cost deployment (Vercel free tier + Supabase)

## 🏗️ Architecture

```mermaid
graph TD
    User[Browser] --> FE[Next.js Frontend<br>localhost:3000 / vercel.app]
    FE --> API[FastAPI Backend<br>/api (Vercel) / localhost:8000]
    API --> DB[Postgres<br>Supabase / Docker DB]
    
    subgraph Local
        FE_L[Frontend:3000] --> BE_L[Backend:8000]
        BE_L --> DB_L[DB:5432]
    end
    subgraph Prod
        FE_P[Vercel FE+API] --> DB_P[Supabase]
    end
```

## 🚀 Quick Start (Docker - Recommended)

1. Clone & setup:
   ```
   git clone <repo> atd-system
   cd atd-system
   cp .env.example .env  # Edit DATABASE_URL if needed (Docker uses defaults)
   ```

2. Run:
   ```
   docker compose up -d
   ```

3. Open [http://localhost:3000](http://localhost:3000)

**Defaults**: DB `user/password@db:5432/attendance_db`, API `http://localhost:8000`.

## 🛠️ Local Development (Standalone)

### Backend
```bash
cd backend
python -m venv venv
# Windows: venv\\Scripts\\activate
# Unix: source venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
uvicorn main:app --reload --port 8000
```
→ [http://localhost:8000/docs](http://localhost:8000/docs)

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Set `NEXT_PUBLIC_API_URL=http://localhost:8000` in `.env.local`.

## ☁️ Production Deployment (100% Free)
Follow `deployment_guide.md`:
1. Supabase → DATABASE_URL.
2. GitHub repo.
3. Vercel import → Add `DATABASE_URL` env var.
4. Live at `your-app.vercel.app`!

## 📁 Structure
```
atd-system/
├── frontend/     # Next.js App Router
├── backend/      # FastAPI + SQLAlchemy
├── api/          # Vercel serverless bridge
├── docker-compose.yml
├── deployment_guide.md
├── vercel.json
├── .gitignore    # This file
└── README.md     # This file
```

## Dependencies
**Frontend** (`frontend/package.json`): Next.js 16, React 19, TypeScript.  
**Backend** (`backend/requirements.txt`): FastAPI, SQLAlchemy, psycopg2-binary, Pydantic.  

## 🤝 Contributing
- Fork & PR.
- See `frontend/AGENTS.md` + `frontend/CLAUDE.md` for AI dev notes.
- `TODO.md` for next steps (e.g., auth, reports).

## 📄 License
MIT - Free to use/modify/deploy.

**Built with ❤️ using VSCode + Docker + Vercel.**

