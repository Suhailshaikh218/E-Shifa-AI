# 🚀 E-Shifa AI - Quick Start Guide

## ✅ CURRENT STATUS

**Backend**: ✅ Running on `http://localhost:8000`
**Database**: ✅ Neon PostgreSQL connected with schema loaded
**API Docs**: ✅ Available at `http://localhost:8000/docs`
**Frontend**: ⚠️ Needs npm install (disk space issue)

---

## 🎯 IMMEDIATE NEXT STEPS

### Step 1: Free Up Disk Space
You need at least **500MB-1GB** free space to install frontend dependencies.

**Quick ways to free space:**
- Empty Recycle Bin
- Delete temp files: `%TEMP%`
- Delete browser cache
- Delete old downloads
- Run Disk Cleanup utility

### Step 2: Install Frontend Dependencies
```bash
cd frontend
npm install
```

### Step 3: Start Frontend
```bash
npm run dev
```

Frontend will run on `http://localhost:3000`

### Step 4: Test Complete Flow
1. Open `http://localhost:3000`
2. Sign up as a customer
3. Book a service: "Mujhe kal morning nurse chahiye"
4. See AI reasoning traces
5. View booking details

---

## 🧪 TESTING BACKEND (Already Working)

### Quick Test
```bash
python test_backend.py
```

### Manual API Tests

**1. Health Check**
```bash
curl http://localhost:8000/health
```

**2. Register User**
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Ahmed Khan",
    "phone_number": "+923001234567",
    "email": "ahmed@example.com",
    "password": "password123",
    "role": "customer"
  }'
```

**3. View API Documentation**
Open: `http://localhost:8000/docs`

---

## 📊 WHAT'S WORKING

### Backend APIs ✅
- `/health` - Health check
- `/api/auth/signup` - User registration
- `/api/auth/login` - User login
- `/api/auth/me` - Get current user
- `/api/bookings/create` - Create booking with AI orchestration
- `/api/bookings/{id}` - Get booking details
- `/api/bookings/` - Get user bookings
- `/api/bookings/feedback` - Submit feedback
- `/api/admin/dashboard` - Admin metrics
- `/api/admin/ai-traces` - AI reasoning logs
- `/api/admin/bookings/live` - Live bookings
- `/api/admin/providers/performance` - Provider stats

### AI Agents ✅
1. **Intent Extraction Agent** - Understands Urdu/English/Roman Urdu
2. **Provider Matching Agent** - 10-factor matching algorithm
3. **Pricing Agent** - Dynamic pricing with transparency
4. **Scheduling Agent** - Conflict prevention
5. **Notification Agent** - Multi-channel notifications
6. **Feedback Agent** - Sentiment analysis

### Database ✅
- 8 tables created
- Sample data loaded (4 users, 2 providers)
- All relationships configured

---

## 🔑 ENVIRONMENT VARIABLES

### Backend (.env) ✅
```env
DATABASE_URL=postgresql://...  # Neon PostgreSQL
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

### Frontend (.env.local) ✅
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=YOUR_GOOGLE_MAPS_API_KEY
```

---

## 🐛 KNOWN ISSUES & FIXES

### Issue 1: Frontend npm install fails (Disk Space)
**Error**: `ENOSPC: no space left on device`
**Fix**: Free up at least 500MB-1GB disk space

### Issue 2: Gemini API model error
**Error**: `models/gemini-1.5-flash is not found`
**Fix**: Updated to use `gemini-pro` model (already fixed)

### Issue 3: Role validation error
**Error**: `customer role not allowed`
**Fix**: Updated schema to accept customer/provider/admin roles (already fixed)

---

## 🎬 DEMO FLOW

Once frontend is running:

1. **Homepage** (`/`)
   - Hero section with service cards
   - Click "Book Now"

2. **Authentication** (`/auth`)
   - Sign up as customer
   - Get JWT token

3. **Book Service** (`/book`)
   - Enter query: "Mujhe kal morning nurse chahiye"
   - Select location on map
   - Click "Find Providers"

4. **AI Processing** (Real-time)
   - Intent extraction with confidence score
   - Provider matching with 10 factors
   - Dynamic pricing breakdown
   - Scheduling with conflict check

5. **Booking Confirmation**
   - View matched providers
   - See AI reasoning traces
   - Confirm booking
   - Get booking number

6. **Booking Details** (`/booking/[id]`)
   - Service status
   - Provider info
   - Price breakdown
   - AI trace logs
   - Submit feedback

7. **Admin Dashboard** (`/admin/dashboard`)
   - Real-time metrics
   - Live bookings
   - AI trace logs
   - Provider performance

---

## 🚀 DEPLOYMENT TO GOOGLE CLOUD

### Prerequisites
- Google Cloud account
- gcloud CLI installed
- Docker installed

### Quick Deploy
```bash
# 1. Build backend
cd backend
docker build -t gcr.io/YOUR_PROJECT/eshifa-backend .
docker push gcr.io/YOUR_PROJECT/eshifa-backend

# 2. Deploy backend
gcloud run deploy eshifa-backend \
  --image gcr.io/YOUR_PROJECT/eshifa-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# 3. Build frontend
cd frontend
docker build -t gcr.io/YOUR_PROJECT/eshifa-frontend .
docker push gcr.io/YOUR_PROJECT/eshifa-frontend

# 4. Deploy frontend
gcloud run deploy eshifa-frontend \
  --image gcr.io/YOUR_PROJECT/eshifa-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

See `DEPLOYMENT_GUIDE.md` for detailed instructions.

---

## 📞 TROUBLESHOOTING

### Backend not starting?
```bash
cd backend
python main.py
# Check for errors in output
```

### Database connection failed?
- Verify `DATABASE_URL` in `backend/.env`
- Check Neon PostgreSQL is accessible
- Run: `python database/load_schema.py`

### Gemini API errors?
- Verify `GEMINI_API_KEY` in `backend/.env`
- Check API key is valid at: https://makersuite.google.com/app/apikey
- Ensure billing is enabled on Google Cloud

### Frontend build errors?
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

## 📚 DOCUMENTATION

- `DEPLOYMENT_GUIDE.md` - Complete deployment instructions
- `ENV_SETUP_GUIDE.md` - Environment variables guide
- `PROJECT_STRUCTURE.md` - File structure documentation
- `FINAL_DEPLOYMENT_STATUS.md` - Current status and issues
- `SYSTEM_ARCHITECTURE.md` - Architecture overview

---

## 🏆 HACKATHON SUBMISSION CHECKLIST

- [x] Backend API working
- [x] Database schema loaded
- [x] AI agents implemented
- [x] Multilingual support
- [x] Provider matching algorithm
- [x] Dynamic pricing
- [x] AI reasoning traces
- [ ] Frontend running (pending disk space)
- [ ] Complete end-to-end flow tested
- [ ] Deployed to Google Cloud
- [ ] Demo video recorded
- [ ] Submission form filled

---

## 💡 TIPS

1. **Test backend first** - Use `python test_backend.py`
2. **Use API docs** - Visit `http://localhost:8000/docs` for interactive testing
3. **Check logs** - Backend terminal shows all AI reasoning traces
4. **Free disk space** - Essential for frontend installation
5. **Deploy early** - Test on Cloud Run before submission deadline

---

**Last Updated**: May 21, 2026
**Status**: Backend Ready ✅ | Frontend Pending ⚠️
