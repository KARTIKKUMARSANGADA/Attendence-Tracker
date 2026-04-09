# 🚀 100% FREE Deployment Guide

Follow this step-by-step guide to get your **Standalone Attendance Tracker** live on the web at zero cost, forever (within free tier limits).

---

## 🏗️ The "Ultimate Free Stack"
- **Hosting**: [Vercel](https://vercel.com) (Frontend + API)
- **Database**: [Supabase](https://supabase.com) (PostgreSQL)
- **CI/CD**: GitHub (Automatic deployments)

---

## Step 1: Set up your Database (Supabase)
1. Go to [Supabase.com](https://supabase.com) and create a free account.
2. Click **New Project** and name it `AttendanceTracker`.
3. Set a strong password and choose a region close to you.
4. Once created, go to **Project Settings** -> **Database**.
5. Copy your **Connection String** (use the "URI" or "Direct" format) – it looks like: `postgresql://postgres:[PASSWORD]@db.kqbvsfapfjiemvjzkdga.supabase.co:5432/postgres`
   > [!IMPORTANT]
   > Replace [YOUR-PASSWORD] with your actual Supabase DB password.

6. **Local Setup**: Copy `.env.example` to `.env` and paste your full DATABASE_URL (with password) there for local testing.

---

## Step 2: Prepare your Code for Vercel
Vercel needs a specific configuration to run both Next.js and FastAPI in the same project.

### 1. The `vercel.json` File
I have already created this in your root folder. It tells Vercel how to route your requests.

### 2. The `api/index.py` File
This is the "bridge" between Vercel and your Python backend. I have also created this for you.

---

## Step 3: Push to GitHub
1. Create a new **Private Repository** on GitHub.
2. Link your local folder to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for deployment"
   git branch -M main
   git remote add origin https://github.com/[YOUR_USERNAME]/[REPO_NAME].git
   git push -u origin main
   ```

---

## Step 4: Deploy on Vercel
1. Go to [Vercel.com](https://vercel.com) and import your GitHub repo.
2. **Framework Preset**: Select "Next.js".
3. **Environment Variables**: Add these in the Vercel dashboard:
   - `DATABASE_URL`: Paste your full Supabase URI from Step 1 (with password – keep it secret!)
   - `NEXT_PUBLIC_API_URL`: `/api` (This makes API calls local to the same domain)

4. Click **Deploy**! 🚀

---

## 🛠️ Post-Deployment Check
- Your site will be at `something.vercel.app`.
- Test the "Clock In" button.
- Check the "Recent History" to ensure Supabase is storing your data.

> [!TIP]
> Since this is a serverless deployment, the backend might take 2-3 seconds to "wake up" the first time you visit the site. This is normal for free hosting!
