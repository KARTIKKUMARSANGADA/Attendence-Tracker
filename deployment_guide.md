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
5. Copy your **Connection String** (URI/Direct format): `postgresql://postgres.YOUR_PASSWORD@db.kqbvsfapfjiemvjzkdga.supabase.co:5432/postgres?sslmode=require`
   > [!IMPORTANT] 
   > - Replace `YOUR_PASSWORD` with your Supabase password.
   > - **SSL Required**: Always append `?sslmode=require` for Vercel serverless.

6. **Local Setup**: Copy `.env.example` to `.env.local`, paste `DATABASE_URL=...`.

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
3. **Environment Variables** (Add to BOTH frontend & backend services, Production+Preview):
   | Key | Value | Scope |
   |-----|-------|-------|
   | `DATABASE_URL` | `postgresql://postgres.YOUR_PASSWORD@db.kqbvsfapfjiemvjzkdga.supabase.co:5432/postgres?sslmode=require` | Secret, both services |
   | `NEXT_PUBLIC_API_URL` | `/_/backend` | Frontend only |

   > Go to Vercel Dashboard → Project → Settings → Environment Variables → Add each.
4. **Deploy**! 🚀 Auto-deploys on future pushes.

---

## 🛠️ Post-Deployment Check
1. **API Health**: `https://YOUR_PROJECT.vercel.app/_/backend/status` → Should return JSON `{status: "Not Started", ...}`
2. **Swagger**: `https://YOUR_PROJECT.vercel.app/_/backend/docs`
3. **Frontend**: `https://YOUR_PROJECT.vercel.app/` → Clock In button, live timer.
4. **Supabase**: Check `attendance` & `attendance_session` tables for data.

**Verify Logs**: Vercel Dashboard → Deployments → Your Deploy → Functions → backend → Logs (look for "Database connected successfully").

> [!TIP] Serverless cold starts: 2-3s first request normal. If frontend APIs fail, ensure `NEXT_PUBLIC_API_URL=/_/backend`.

## Troubleshooting
- Error \"multiple services\"? Ensure latest `vercel.json`.
- Redeploy: Push to GitHub → Vercel auto-builds.


