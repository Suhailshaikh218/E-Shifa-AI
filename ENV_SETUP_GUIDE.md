# 🔑 Environment Variables Setup Guide

## Quick Reference for API Keys & Configuration

---

## 📋 Required API Keys

### 1. Google Gemini API Key (FREE!)

**Where to get:**
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Select your Google Cloud project
4. Copy the key

**Format:**
```
AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**Free Tier:**
- ✅ 60 requests per minute
- ✅ 1,500 requests per day
- ✅ No credit card required

**Where to use:**
```env
# backend/.env
GEMINI_API_KEY=AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

---

## 🗄️ Database Configuration

### Local Development

**PostgreSQL Connection String:**
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/eshifa
```

**Format Breakdown:**
```
postgresql://[username]:[password]@[host]:[port]/[database]
```

**Example:**
```
postgresql://postgres:mypass123@localhost:5432/eshifa
```

### Production (Google Cloud SQL)

**Connection String:**
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@/eshifa?host=/cloudsql/PROJECT_ID:REGION:INSTANCE_NAME
```

**Example:**
```
DATABASE_URL=postgresql://postgres:StrongPass123@/eshifa?host=/cloudsql/my-project:asia-south1:eshifa-db
```

**How to get Cloud SQL connection name:**
```bash
gcloud sql instances describe eshifa-db --format="value(connectionName)"
```

---

## 🔐 Security Configuration

### Secret Key Generation

**Generate a strong secret key:**

**Python:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Output Example:**
```
xK9mP2nQ5rT8wV1yZ4bC7dF0gH3jL6mN9pR2sU5vX8
```

**Where to use:**
```env
# backend/.env
SECRET_KEY=xK9mP2nQ5rT8wV1yZ4bC7dF0gH3jL6mN9pR2sU5vX8
```

**⚠️ IMPORTANT:**
- Never use the example key
- Generate a new one for each environment
- Keep it secret (don't commit to git)
- Minimum 32 characters

---

## 🌐 CORS Configuration

### Local Development

```env
CORS_ORIGINS=http://localhost:3000
```

### Production

```env
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app
```

### Multiple Domains

```env
CORS_ORIGINS=http://localhost:3000,https://staging.vercel.app,https://production.vercel.app
```

**Format:**
- Comma-separated (no spaces)
- Include protocol (http:// or https://)
- No trailing slash

---

## 📁 Complete .env Files

### Backend (.env)

**Location:** `backend/.env`

```env
# ============================================
# DATABASE
# ============================================
DATABASE_URL=postgresql://postgres:password@localhost:5432/eshifa

# ============================================
# SECURITY
# ============================================
SECRET_KEY=xK9mP2nQ5rT8wV1yZ4bC7dF0gH3jL6mN9pR2sU5vX8
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# ============================================
# AI
# ============================================
GEMINI_API_KEY=AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ============================================
# CORS
# ============================================
CORS_ORIGINS=http://localhost:3000

# ============================================
# APP
# ============================================
APP_NAME=E-Shifa AI
APP_VERSION=2.0.0
DEBUG=True
```

### Frontend (.env.local)

**Location:** `frontend/.env.local`

```env
# ============================================
# API
# ============================================
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🚀 Production Configuration

### Backend (.env) - Production

```env
# ============================================
# DATABASE (Cloud SQL)
# ============================================
DATABASE_URL=postgresql://postgres:StrongPass123@/eshifa?host=/cloudsql/my-project:asia-south1:eshifa-db

# ============================================
# SECURITY
# ============================================
SECRET_KEY=PRODUCTION_SECRET_KEY_DIFFERENT_FROM_DEV
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# ============================================
# AI
# ============================================
GEMINI_API_KEY=AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ============================================
# CORS (Production Domain)
# ============================================
CORS_ORIGINS=https://your-app.vercel.app

# ============================================
# APP
# ============================================
APP_NAME=E-Shifa AI
APP_VERSION=2.0.0
DEBUG=False
```

### Frontend (.env.local) - Production

```env
# ============================================
# API (Cloud Run URL)
# ============================================
NEXT_PUBLIC_API_URL=https://eshifa-backend-xxxxx-as.a.run.app
```

---

## 🔍 How to Find Your Values

### 1. Gemini API Key
```
URL: https://makersuite.google.com/app/apikey
Steps: Create API Key → Copy
```

### 2. Database Password
```
Local: Your PostgreSQL password
Cloud SQL: Set when creating instance
```

### 3. Secret Key
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Backend URL (Production)
```bash
gcloud run services describe eshifa-backend --region=asia-south1 --format="value(status.url)"
```

### 5. Cloud SQL Connection Name
```bash
gcloud sql instances describe eshifa-db --format="value(connectionName)"
```

---

## ✅ Verification Checklist

### Backend
- [ ] ✅ DATABASE_URL is correct
- [ ] ✅ SECRET_KEY is generated (not example)
- [ ] ✅ GEMINI_API_KEY is valid
- [ ] ✅ CORS_ORIGINS includes frontend URL
- [ ] ✅ DEBUG=False in production

### Frontend
- [ ] ✅ NEXT_PUBLIC_API_URL points to backend
- [ ] ✅ Uses HTTPS in production
- [ ] ✅ No trailing slash in URL

---

## 🐛 Common Issues

### Issue 1: "Database connection failed"

**Check:**
```bash
# Test PostgreSQL connection
psql -U postgres -d eshifa -c "SELECT 1;"
```

**Fix:**
- Verify username/password
- Check database exists
- Ensure PostgreSQL is running

### Issue 2: "Gemini API error"

**Check:**
```bash
# Test API key
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'
```

**Fix:**
- Verify API key is correct
- Check API is enabled in Google Cloud
- Ensure billing is enabled (if using paid tier)

### Issue 3: "CORS error"

**Check:**
```bash
# Check backend CORS settings
curl -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -X OPTIONS http://localhost:8000/api/auth/login
```

**Fix:**
- Add frontend URL to CORS_ORIGINS
- Include protocol (http:// or https://)
- No trailing slash

### Issue 4: "Frontend can't connect to backend"

**Check:**
```bash
# Test backend is running
curl http://localhost:8000/health
```

**Fix:**
- Verify NEXT_PUBLIC_API_URL is correct
- Check backend is running
- Ensure no firewall blocking

---

## 📝 Environment Variables Reference

### Backend Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| DATABASE_URL | ✅ Yes | - | PostgreSQL connection string |
| SECRET_KEY | ✅ Yes | - | JWT secret key (32+ chars) |
| ALGORITHM | ✅ Yes | HS256 | JWT algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | ✅ Yes | 1440 | Token expiration (24 hours) |
| GEMINI_API_KEY | ✅ Yes | - | Google Gemini API key |
| CORS_ORIGINS | ✅ Yes | - | Allowed frontend origins |
| APP_NAME | ❌ No | E-Shifa AI | Application name |
| APP_VERSION | ❌ No | 2.0.0 | Application version |
| DEBUG | ❌ No | True | Debug mode (False in prod) |

### Frontend Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| NEXT_PUBLIC_API_URL | ✅ Yes | - | Backend API URL |

---

## 🔒 Security Best Practices

### DO ✅
- ✅ Use strong, random SECRET_KEY
- ✅ Keep API keys secret
- ✅ Use environment variables
- ✅ Different keys for dev/prod
- ✅ Set DEBUG=False in production
- ✅ Use HTTPS in production
- ✅ Restrict CORS to your domain

### DON'T ❌
- ❌ Commit .env files to git
- ❌ Share API keys publicly
- ❌ Use example/default keys
- ❌ Hardcode secrets in code
- ❌ Use HTTP in production
- ❌ Allow CORS from all origins (*)

---

## 🎯 Quick Setup Commands

### 1. Copy Example Files
```bash
# Backend
cp backend/.env.example backend/.env

# Frontend
cp frontend/.env.local.example frontend/.env.local
```

### 2. Generate Secret Key
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Update .env Files
```bash
# Edit backend/.env
nano backend/.env

# Edit frontend/.env.local
nano frontend/.env.local
```

### 4. Verify Configuration
```bash
# Test backend
cd backend
python main.py

# Test frontend (new terminal)
cd frontend
npm run dev
```

---

## 📞 Need Help?

### Get Gemini API Key
https://makersuite.google.com/app/apikey

### Google Cloud Documentation
https://cloud.google.com/docs

### PostgreSQL Documentation
https://www.postgresql.org/docs/

### Deployment Guide
See `DEPLOYMENT_GUIDE.md`

---

## ✅ Final Checklist

Before running:
- [ ] ✅ Copied .env.example to .env
- [ ] ✅ Added Gemini API key
- [ ] ✅ Generated SECRET_KEY
- [ ] ✅ Updated DATABASE_URL
- [ ] ✅ Set CORS_ORIGINS
- [ ] ✅ Updated frontend API URL
- [ ] ✅ Tested database connection
- [ ] ✅ Verified API key works

**You're ready to go! 🚀**

