# 🚀 E-Shifa AI - Quick Start Guide

## Get the Hackathon MVP Running in 10 Minutes

---

## ⚡ Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))

---

## 📦 Step 1: Clone & Setup Database

```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE eshifa;
\q

# Run schema
psql -U postgres -d eshifa -f database/mvp_schema.sql
```

---

## 🐍 Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "DATABASE_URL=postgresql://postgres:password@localhost:5432/eshifa" > .env
echo "GEMINI_API_KEY=your_gemini_api_key_here" >> .env
echo "SECRET_KEY=hackathon_secret_key_2026" >> .env
echo "ALGORITHM=HS256" >> .env
echo "ACCESS_TOKEN_EXPIRE_MINUTES=1440" >> .env
echo "CORS_ORIGINS=http://localhost:3000" >> .env

# Start backend
python main.py
```

✅ Backend running on: **http://localhost:8000**

---

## ⚛️ Step 3: Frontend Setup

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start frontend
npm run dev
```

✅ Frontend running on: **http://localhost:3000**

---

## 🎮 Step 4: Test the System

### 1. Register a Customer

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+923001111111",
    "full_name": "Test Customer",
    "password": "test123",
    "role": "customer"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+923001111111",
    "password": "test123"
  }'
```

Copy the `access_token` from response.

### 3. Create a Booking

```bash
curl -X POST http://localhost:8000/api/bookings/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "user_query": "I need a home nurse tomorrow at 10 AM",
    "location": {
      "lat": 24.8607,
      "lng": 67.0011,
      "address": "Karachi, Pakistan"
    }
  }'
```

---

## 🌐 Step 5: Access the Application

### Customer Flow
1. Go to: **http://localhost:3000**
2. Click "Book Service Now"
3. Select a service
4. Enter your request (try in Urdu!)
5. Watch AI agents work
6. See provider matching
7. Confirm booking

### Admin Dashboard
1. Go to: **http://localhost:3000/admin/dashboard**
2. Login with admin credentials
3. View real-time metrics
4. See AI reasoning traces
5. Monitor live bookings

---

## 🎯 Demo Scenarios

### Scenario 1: Routine Home Nurse
```
Query: "Mujhe ghar pe nurse chahiye kal subah 10 baje"
Expected: Routine urgency, home_nurse service, tomorrow 10 AM
```

### Scenario 2: Urgent Doctor Visit
```
Query: "I need a doctor urgently, my father has high fever"
Expected: Urgent urgency, doctor_visit service, ASAP
```

### Scenario 3: Emergency Ambulance
```
Query: "Emergency! Need ambulance immediately"
Expected: Emergency urgency, ambulance service, immediate
```

---

## 📊 API Documentation

Once backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
pg_isready

# Check database exists
psql -U postgres -l | grep eshifa
```

### Gemini API Error
```bash
# Verify API key in .env
cat backend/.env | grep GEMINI_API_KEY

# Test API key
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'
```

### Frontend Not Connecting
```bash
# Check backend is running
curl http://localhost:8000/health

# Check CORS settings in backend/.env
cat backend/.env | grep CORS_ORIGINS
```

---

## 🎥 Quick Demo Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Database has sample data
- [ ] Gemini API key configured
- [ ] Can create booking
- [ ] AI traces visible
- [ ] Admin dashboard accessible
- [ ] Pricing breakdown shows
- [ ] Provider matching works

---

## 📱 Test Credentials

### Customer
- Phone: `+923001234567`
- Password: `password123`

### Provider
- Phone: `+923009876543`
- Password: `password123`

### Admin
- Phone: `+923005555555`
- Password: `admin123`

---

## 🚀 Production Deployment

### Backend (Google Cloud Run)
```bash
gcloud run deploy eshifa-backend \
  --source ./backend \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated
```

### Frontend (Vercel)
```bash
cd frontend
vercel --prod
```

---

## 📞 Need Help?

- Check logs: `backend/logs/` and browser console
- API docs: http://localhost:8000/docs
- Database: `psql -U postgres -d eshifa`

---

## ✅ Success Indicators

You're ready for the demo when:

1. ✅ Homepage loads with 6 services
2. ✅ Can create booking with multilingual input
3. ✅ AI traces show in booking details
4. ✅ Admin dashboard shows metrics
5. ✅ Provider matching returns top 3
6. ✅ Pricing breakdown is transparent
7. ✅ Feedback system works

---

**Time to MVP: ~10 minutes** ⚡

**Demo Duration: 5 minutes** 🎥

**Wow Factor: 100%** 🚀

