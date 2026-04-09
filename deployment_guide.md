# 🚀 100% FREE Multi-Service Deployment Guide (Updated for experimentalServices)

Follow this step-by-step guide to deploy your **Standalone Attendance Tracker** as multi-service monorepo on Vercel at zero cost (free tier).

---

## 🏗️ The \"Ultimate Free Stack\"
- **Hosting**: [Vercel](https://vercel.com) (Frontend + Backend services)
- **Database**: [Supabase](https://supabase.com) (PostgreSQL)
- **CI/CD**: GitHub (Automatic deployments)

---

## Step 1: Set up your Database (Supabase)
1. Go to [Supabase.com](https://supabase.com) and create a free account.
2. Click **New Project** and name it `AttendanceTracker`.
3. Set a strong password and choose a region close to you.
4. Go to **Project Settings** -> **Database**.
5. Copy your **Connection String** (URI/Direct format): `postgresql://postgres:[PASSWORD]@db...supabase.co:5432/postgres`
   > [!IMPORTANT] Replace [YOUR-PASSWORD] with actual password.

6. **Local Setup**: Copy `.env.example` to `.env`, paste DATABASE_URL.

---

## Step 2: Code is Prepared for Vercel (Multi-Service)
- `vercel.json` configured with `experimentalServices`:
  - **frontend** (Next.js): Serves `/` (UI and pages).
  - **backend** (FastAPI): Serves `/_/backend/*` (API endpoints).
- `api/index.py` deprecated (backend now direct service).

---

## Step 3: Push to GitHub
```bash
git add .
git commit -m \"Configure multi-service Vercel deployment\"
git push
```
(If new repo: `git init`, `git branch -M main`, `git remote add origin https://github.com/[USER]/[REPO].git`, `git push -u origin main`.)

---

## Step 4: Deploy on Vercel
1. [Vercel.com](https://vercel.com) → Import GitHub repo.
2. **Framework Preset**: Other/Empty (multi-service).
3. **Environment Variables** (both services):
   - `DATABASE_URL`: Full Supabase URI (secret).
   - `NEXT_PUBLIC_API_URL`: `/_/backend` (for frontend API calls).
4. **Deploy**! 🚀 Auto-deploys on future pushes.

---

## 🛠️ Post-Deployment Check
- Site: `something.vercel.app` (frontend `/`).
- API: `something.vercel.app/_/backend/docs` (FastAPI Swagger).
- Test \"Clock In\" (should hit backend via `/_/backend`).
- Recent History → Supabase data.

> [!TIP] Serverless cold starts: 2-3s first request normal. If frontend APIs fail, ensure `NEXT_PUBLIC_API_URL=/_/backend`.

## Troubleshooting
- Error \"multiple services\"? Ensure latest `vercel.json`.
- Redeploy: Push to GitHub → Vercel auto-builds.


