# 🚀 E-Shifa AI - Complete Deployment Guide

## Production Deployment on Google Cloud

---

## 📋 Prerequisites

1. ✅ Google Cloud Account
2. ✅ Google Cloud CLI installed
3. ✅ Gemini API Key
4. ✅ PostgreSQL database (Cloud SQL)
5. ✅ Vercel account (for frontend)

---

## 🔑 Step 1: Get API Keys

### 1.1 Google Gemini API Key

**Free Tier Available!**

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Select your Google Cloud project (or create new)
4. Copy the API key
5. **Important**: Keep it secret!

**Example Key Format:**
```
AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### 1.2 Generate Secret Key

Run this in terminal:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Example Output:**
```
xK9mP2nQ5rT8wV1yZ4bC7dF0gH3jL6mN9pR2sU5vX8
```

---

## 🗄️ Step 2: Setup PostgreSQL Database

### Option A: Google Cloud SQL (Recommended)

1. **Create Cloud SQL Instance**
```bash
gcloud sql instances create eshifa-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=asia-south1
```

2. **Set Root Password**
```bash
gcloud sql users set-password postgres \
  --instance=eshifa-db \
  --password=YOUR_STRONG_PASSWORD
```

3. **Create Database**
```bash
gcloud sql databases create eshifa --instance=eshifa-db
```

4. **Get Connection String**
```bash
gcloud sql instances describe eshifa-db --format="value(connectionName)"
```

**Output Example:**
```
your-project-id:asia-south1:eshifa-db
```

**Connection String Format:**
```
postgresql://postgres:YOUR_PASSWORD@/eshifa?host=/cloudsql/your-project-id:asia-south1:eshifa-db
```

### Option B: Local PostgreSQL (Development)

```bash
# Create database
psql -U postgres
CREATE DATABASE eshifa;
\q

# Run schema
psql -U postgres -d eshifa -f database/mvp_schema.sql
```

**Connection String:**
```
postgresql://postgres:password@localhost:5432/eshifa
```

---

## 🐍 Step 3: Backend Environment Variables

### Create `backend/.env` file:

```bash
cd backend
nano .env
```

### Paste this configuration:

```env
# ============================================
# DATABASE CONFIGURATION
# ============================================

# For Local Development:
DATABASE_URL=postgresql://postgres:password@localhost:5432/eshifa

# For Google Cloud SQL (Production):
# DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@/eshifa?host=/cloudsql/PROJECT_ID:REGION:INSTANCE_NAME

# ============================================
# SECURITY CONFIGURATION
# ============================================

# Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=xK9mP2nQ5rT8wV1yZ4bC7dF0gH3jL6mN9pR2sU5vX8

# JWT Algorithm (don't change)
ALGORITHM=HS256

# Token expiration (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# ============================================
# AI CONFIGURATION
# ============================================

# Get from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ============================================
# CORS CONFIGURATION
# ============================================

# For Local Development:
CORS_ORIGINS=http://localhost:3000

# For Production (add your Vercel domain):
# CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app

# ============================================
# APPLICATION CONFIGURATION
# ============================================

APP_NAME=E-Shifa AI
APP_VERSION=2.0.0
DEBUG=False

# ============================================
# OPTIONAL: Google Maps API (Future)
# ============================================

# GOOGLE_MAPS_API_KEY=your_maps_api_key_here
```

---

## ⚛️ Step 4: Frontend Environment Variables

### Create `frontend/.env.local` file:

```bash
cd frontend
nano .env.local
```

### Paste this configuration:

```env
# ============================================
# API CONFIGURATION
# ============================================

# For Local Development:
NEXT_PUBLIC_API_URL=http://localhost:8000

# For Production (after deploying backend):
# NEXT_PUBLIC_API_URL=https://your-backend-url.run.app

# ============================================
# OPTIONAL: Google Maps (Future)
# ============================================

# NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_maps_api_key_here
```

---

## 🚀 Step 5: Deploy Backend to Google Cloud Run

### 5.1 Install Google Cloud CLI

**Windows:**
```bash
# Download from: https://cloud.google.com/sdk/docs/install
```

**Mac:**
```bash
brew install google-cloud-sdk
```

**Linux:**
```bash
curl https://sdk.cloud.google.com | bash
```

### 5.2 Login to Google Cloud

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 5.3 Enable Required APIs

```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable sqladmin.googleapis.com
```

### 5.4 Deploy Backend

```bash
cd backend

# Deploy to Cloud Run
gcloud run deploy eshifa-backend \
  --source . \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars "DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@/eshifa?host=/cloudsql/PROJECT_ID:REGION:INSTANCE_NAME" \
  --set-env-vars "SECRET_KEY=YOUR_SECRET_KEY" \
  --set-env-vars "GEMINI_API_KEY=YOUR_GEMINI_KEY" \
  --set-env-vars "CORS_ORIGINS=https://your-app.vercel.app" \
  --add-cloudsql-instances PROJECT_ID:REGION:INSTANCE_NAME
```

### 5.5 Get Backend URL

After deployment, you'll get a URL like:
```
https://eshifa-backend-xxxxx-as.a.run.app
```

**Copy this URL!** You'll need it for frontend.

---

## 🌐 Step 6: Deploy Frontend to Vercel

### 6.1 Install Vercel CLI

```bash
npm install -g vercel
```

### 6.2 Login to Vercel

```bash
vercel login
```

### 6.3 Update Frontend Environment

```bash
cd frontend

# Update .env.local with backend URL
echo "NEXT_PUBLIC_API_URL=https://eshifa-backend-xxxxx-as.a.run.app" > .env.local
```

### 6.4 Deploy to Vercel

```bash
vercel --prod
```

**Follow the prompts:**
- Set up and deploy? **Y**
- Which scope? **Your account**
- Link to existing project? **N**
- Project name? **eshifa-ai**
- Directory? **./frontend**
- Override settings? **N**

### 6.5 Set Environment Variables in Vercel

```bash
vercel env add NEXT_PUBLIC_API_URL production
# Paste: https://eshifa-backend-xxxxx-as.a.run.app
```

**Or via Vercel Dashboard:**
1. Go to: https://vercel.com/dashboard
2. Select your project
3. Settings → Environment Variables
4. Add: `NEXT_PUBLIC_API_URL` = `https://your-backend-url.run.app`

---

## 🗄️ Step 7: Initialize Database

### 7.1 Connect to Cloud SQL

```bash
gcloud sql connect eshifa-db --user=postgres
```

### 7.2 Run Schema

```sql
-- Copy contents of database/mvp_schema.sql and paste
```

**Or upload file:**
```bash
gcloud sql import sql eshifa-db gs://your-bucket/mvp_schema.sql \
  --database=eshifa
```

---

## ✅ Step 8: Verify Deployment

### 8.1 Test Backend

```bash
curl https://eshifa-backend-xxxxx-as.a.run.app/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "app": "E-Shifa AI",
  "version": "2.0.0",
  "database": "connected",
  "ai_engine": "operational"
}
```

### 8.2 Test Frontend

Open: `https://your-app.vercel.app`

**Check:**
- ✅ Landing page loads
- ✅ Can navigate to booking page
- ✅ Can see 6 services
- ✅ No console errors

### 8.3 Test Complete Flow

1. Register a user
2. Create a booking
3. Check AI traces
4. View admin dashboard

---

## 🔒 Step 9: Security Checklist

### Backend Security

- [ ] ✅ Strong SECRET_KEY (32+ characters)
- [ ] ✅ GEMINI_API_KEY not exposed in code
- [ ] ✅ DATABASE_URL not in git
- [ ] ✅ CORS_ORIGINS set to production domain only
- [ ] ✅ DEBUG=False in production
- [ ] ✅ Cloud SQL has strong password
- [ ] ✅ Cloud SQL allows only Cloud Run connection

### Frontend Security

- [ ] ✅ API URL uses HTTPS
- [ ] ✅ No sensitive data in client code
- [ ] ✅ Environment variables prefixed with NEXT_PUBLIC_

### Database Security

- [ ] ✅ Strong postgres password
- [ ] ✅ Cloud SQL private IP (optional)
- [ ] ✅ Automated backups enabled
- [ ] ✅ SSL connections enforced

---

## 📊 Step 10: Monitoring & Logs

### Backend Logs (Cloud Run)

```bash
# View logs
gcloud run services logs read eshifa-backend --region=asia-south1

# Follow logs (real-time)
gcloud run services logs tail eshifa-backend --region=asia-south1
```

### Frontend Logs (Vercel)

1. Go to: https://vercel.com/dashboard
2. Select project
3. Click "Logs" tab

### Database Logs (Cloud SQL)

```bash
gcloud sql operations list --instance=eshifa-db
```

---

## 💰 Step 11: Cost Optimization

### Free Tier Limits

**Google Cloud Run:**
- 2 million requests/month (FREE)
- 360,000 GB-seconds/month (FREE)
- 180,000 vCPU-seconds/month (FREE)

**Cloud SQL:**
- db-f1-micro: ~$7/month
- 10 GB storage: ~$1.70/month

**Vercel:**
- Hobby plan: FREE
- 100 GB bandwidth/month
- Unlimited deployments

**Gemini API:**
- Free tier: 60 requests/minute
- Paid: $0.00025 per 1K characters

**Total Estimated Cost:** ~$10-15/month

### Cost Saving Tips

1. **Use Cloud Run** (scales to zero)
2. **Use db-f1-micro** for Cloud SQL
3. **Enable Cloud SQL auto-pause** (if low traffic)
4. **Use Vercel free tier** (sufficient for MVP)
5. **Monitor Gemini API usage**

---

## 🔄 Step 12: Update Deployment

### Update Backend

```bash
cd backend
gcloud run deploy eshifa-backend \
  --source . \
  --region asia-south1
```

### Update Frontend

```bash
cd frontend
vercel --prod
```

### Update Database Schema

```bash
# Connect to Cloud SQL
gcloud sql connect eshifa-db --user=postgres

# Run new migrations
\i /path/to/new_migration.sql
```

---

## 🐛 Troubleshooting

### Backend Not Starting

**Check logs:**
```bash
gcloud run services logs read eshifa-backend --region=asia-south1 --limit=50
```

**Common issues:**
- ❌ Wrong DATABASE_URL format
- ❌ Missing GEMINI_API_KEY
- ❌ Cloud SQL instance not connected
- ❌ Wrong SECRET_KEY

### Frontend Can't Connect to Backend

**Check:**
- ❌ NEXT_PUBLIC_API_URL is correct
- ❌ Backend CORS_ORIGINS includes frontend domain
- ❌ Backend is deployed and running
- ❌ HTTPS (not HTTP) in production

### Database Connection Failed

**Check:**
- ❌ Cloud SQL instance is running
- ❌ Database name is correct
- ❌ Password is correct
- ❌ Cloud Run has Cloud SQL connection enabled

### Gemini API Errors

**Check:**
- ❌ API key is valid
- ❌ API key has Gemini API enabled
- ❌ Not exceeding rate limits
- ❌ Billing enabled (if using paid tier)

---

## 📱 Step 13: Custom Domain (Optional)

### Backend Custom Domain

```bash
gcloud run domain-mappings create \
  --service=eshifa-backend \
  --domain=api.yourdomain.com \
  --region=asia-south1
```

### Frontend Custom Domain

1. Go to Vercel Dashboard
2. Project Settings → Domains
3. Add domain: `yourdomain.com`
4. Follow DNS instructions

---

## 🎯 Quick Reference

### Environment Variables Summary

**Backend (.env):**
```env
DATABASE_URL=postgresql://...
SECRET_KEY=your_secret_key
GEMINI_API_KEY=AIzaSy...
CORS_ORIGINS=https://your-app.vercel.app
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=https://your-backend.run.app
```

### Deployment Commands

**Backend:**
```bash
gcloud run deploy eshifa-backend --source . --region asia-south1
```

**Frontend:**
```bash
vercel --prod
```

### URLs

- **Backend**: https://eshifa-backend-xxxxx-as.a.run.app
- **Frontend**: https://your-app.vercel.app
- **API Docs**: https://eshifa-backend-xxxxx-as.a.run.app/docs

---

## ✅ Deployment Checklist

- [ ] ✅ Google Cloud project created
- [ ] ✅ Gemini API key obtained
- [ ] ✅ Cloud SQL instance created
- [ ] ✅ Database schema loaded
- [ ] ✅ Backend .env configured
- [ ] ✅ Backend deployed to Cloud Run
- [ ] ✅ Frontend .env.local configured
- [ ] ✅ Frontend deployed to Vercel
- [ ] ✅ CORS configured correctly
- [ ] ✅ Complete flow tested
- [ ] ✅ Monitoring enabled
- [ ] ✅ Backups configured

---

## 🎉 Success!

Your E-Shifa AI is now **LIVE** and **production-ready**! 🚀

**Share your demo:**
- Frontend: https://your-app.vercel.app
- API Docs: https://your-backend.run.app/docs

---

**Need Help?**
- Google Cloud: https://cloud.google.com/docs
- Vercel: https://vercel.com/docs
- Gemini API: https://ai.google.dev/docs

