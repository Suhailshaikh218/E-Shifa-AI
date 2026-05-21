# 🚀 Deploy E-Shifa AI to Google Cloud (Skip Local Frontend)

## Why This Approach?
- Your backend is 100% working ✅
- Local disk space is insufficient for npm install
- Google Cloud Run has its own build environment
- Better for hackathon submission (production URL)

---

## OPTION 1: Deploy Using Google Cloud Console (Easiest)

### Step 1: Create Google Cloud Project
1. Go to: https://console.cloud.google.com/
2. Click "New Project"
3. Name: `eshifa-ai-hackathon`
4. Click "Create"

### Step 2: Enable Required APIs
```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 3: Deploy Backend
```bash
cd backend

# Build and deploy in one command
gcloud run deploy eshifa-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL="postgresql://neondb_owner:npg_xxxxxxxxx@ep-xxxxxxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require" \
  --set-env-vars GEMINI_API_KEY="YOUR_GEMINI_API_KEY" \
  --set-env-vars SECRET_KEY="your-secret-key-here-change-in-production" \
  --set-env-vars ALGORITHM="HS256" \
  --set-env-vars ACCESS_TOKEN_EXPIRE_MINUTES="10080"
```

**Note**: Replace the DATABASE_URL with your actual Neon connection string from `backend/.env`

### Step 4: Deploy Frontend
```bash
cd frontend

# Build and deploy in one command
gcloud run deploy eshifa-frontend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars NEXT_PUBLIC_API_URL="https://eshifa-backend-xxxxxxxxx-uc.a.run.app" \
  --set-env-vars NEXT_PUBLIC_GOOGLE_MAPS_API_KEY="YOUR_GOOGLE_MAPS_API_KEY"
```

**Note**: Replace NEXT_PUBLIC_API_URL with the backend URL from Step 3

---

## OPTION 2: Use Docker (If gcloud source deploy fails)

### Backend Dockerfile (already exists)
```bash
cd backend
docker build -t gcr.io/eshifa-ai-hackathon/backend .
docker push gcr.io/eshifa-ai-hackathon/backend

gcloud run deploy eshifa-backend \
  --image gcr.io/eshifa-ai-hackathon/backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Frontend Dockerfile (already exists)
```bash
cd frontend
docker build -t gcr.io/eshifa-ai-hackathon/frontend .
docker push gcr.io/eshifa-ai-hackathon/frontend

gcloud run deploy eshifa-frontend \
  --image gcr.io/eshifa-ai-hackathon/frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## OPTION 3: Deploy Backend Only (Quickest for Demo)

Since backend is working perfectly, deploy just the backend and use the API documentation as your demo:

```bash
cd backend
gcloud run deploy eshifa-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

Then access:
- API: `https://eshifa-backend-xxxxx-uc.a.run.app`
- Docs: `https://eshifa-backend-xxxxx-uc.a.run.app/docs`

You can demo the entire AI orchestration through the interactive API docs!

---

## ALTERNATIVE: Use Vercel for Frontend (Free & Easy)

If Google Cloud is complex, use Vercel for frontend:

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Deploy Frontend
```bash
cd frontend
vercel --prod
```

Vercel will:
- Build the frontend in the cloud (no local disk space needed)
- Deploy automatically
- Give you a production URL

---

## QUICKEST PATH TO DEMO (Recommended)

### 1. Deploy Backend to Google Cloud Run (5 minutes)
```bash
cd backend
gcloud run deploy eshifa-backend --source . --region us-central1 --allow-unauthenticated
```

### 2. Use API Documentation for Demo
- Open: `https://your-backend-url.run.app/docs`
- Show interactive API testing
- Demonstrate AI orchestration
- Show AI reasoning traces in responses

### 3. Show Code & Architecture
- Show `backend/app/services/ai_agents.py` (6 AI agents)
- Show `database/mvp_schema.sql` (clean schema)
- Show `backend/app/api/bookings.py` (orchestration)

---

## DEMO SCRIPT (Using API Docs)

### 1. Health Check
```
GET /health
```
Shows: System is operational

### 2. Register User
```
POST /api/auth/signup
{
  "full_name": "Ahmed Khan",
  "phone_number": "+923001234567",
  "email": "ahmed@example.com",
  "password": "password123",
  "role": "customer"
}
```
Shows: User registration with JWT token

### 3. Create Booking (Main Demo)
```
POST /api/bookings/create
Authorization: Bearer <token>
{
  "user_query": "Mujhe kal morning nurse chahiye injection ke liye",
  "location": {
    "lat": 24.8607,
    "lng": 67.0011,
    "address": "Karachi, Pakistan"
  }
}
```

Shows:
- Intent extraction (multilingual)
- Provider matching (10 factors)
- Dynamic pricing (transparent)
- Scheduling (conflict prevention)
- AI reasoning traces (complete transparency)

### 4. Get Booking Details
```
GET /api/bookings/{booking_id}
```
Shows: Complete booking with AI traces

### 5. Admin Dashboard
```
GET /api/admin/dashboard
```
Shows: Real-time metrics

---

## COST ESTIMATE

### Google Cloud Run
- **Free tier**: 2 million requests/month
- **Cost**: $0 for hackathon demo
- **Scaling**: Automatic

### Vercel (Frontend)
- **Free tier**: Unlimited deployments
- **Cost**: $0
- **Performance**: Global CDN

---

## TROUBLESHOOTING

### gcloud not found?
Install: https://cloud.google.com/sdk/docs/install

### Docker not found?
Install: https://docs.docker.com/get-docker/

### Authentication errors?
```bash
gcloud auth login
gcloud config set project eshifa-ai-hackathon
```

---

## WHAT TO SUBMIT

### 1. Backend URL
`https://eshifa-backend-xxxxx-uc.a.run.app`

### 2. API Documentation
`https://eshifa-backend-xxxxx-uc.a.run.app/docs`

### 3. GitHub Repository
Push your code to GitHub

### 4. Demo Video
Record 5-10 minute video showing:
- API documentation interface
- Creating a booking with Urdu query
- AI reasoning traces in response
- Provider matching algorithm
- Dynamic pricing breakdown
- Admin dashboard metrics

### 5. Architecture Diagram
Show the 6 AI agents and orchestration flow

---

## SUCCESS METRICS

✅ Backend deployed and accessible
✅ API documentation working
✅ Can create bookings via API
✅ AI reasoning traces visible
✅ Multilingual input working
✅ Provider matching functional
✅ Dynamic pricing transparent
✅ Admin dashboard accessible

---

**BOTTOM LINE**: You don't need the frontend running locally! Deploy the backend to Cloud Run and use the interactive API docs (`/docs`) for your demo. It's actually more impressive to show the raw AI orchestration!

