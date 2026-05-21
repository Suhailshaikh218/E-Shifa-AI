# 🏥 E-Shifa AI - Hackathon MVP

## AI-Powered Home Healthcare Service Orchestrator for Pakistan's Informal Economy

---

## 🎯 Project Overview

E-Shifa AI is an intelligent home healthcare service platform that uses **multi-agent AI orchestration** to match customers with healthcare providers. Built for the **"AI Service Orchestrator for Informal Economy"** hackathon challenge.

### Key Innovation
- **6 AI Agents** working in sequence (Antigravity-style workflow)
- **10-factor provider matching** algorithm
- **Dynamic pricing** with transparency
- **Multilingual support** (Urdu, Roman Urdu, English)
- **Real-time AI reasoning traces** for demo visibility

---

## 🚀 Core Services

1. **👩‍⚕️ Home Nurse** - Professional nursing care at home
2. **👨‍⚕️ Doctor Home Visit** - Doctor consultation at doorstep
3. **🤝 Caregiver** - Elderly and patient care services
4. **🏃 Physiotherapist** - Physical therapy at home
5. **🧪 Lab Sample Collection** - Blood/urine sample pickup
6. **🚑 Ambulance** - Emergency medical transport

---

## 🤖 AI Agent Architecture

### Complete Workflow
```
User Request (Multilingual)
    ↓
[Agent 1: Intent Extraction]
    ↓
[Agent 2: Provider Matching (10 factors)]
    ↓
[Agent 3: Dynamic Pricing]
    ↓
[Agent 4: Scheduling]
    ↓
[Agent 5: Notifications]
    ↓
Booking Confirmed
    ↓
[Agent 6: Feedback & Reputation]
```

### Agent Details

#### 1. Intent Extraction Agent
- Detects language (Urdu/Roman Urdu/English)
- Extracts service type, urgency, time preference
- Confidence scoring (0-1)
- **AI Model**: Google Gemini 1.5 Flash

#### 2. Provider Matching Agent
- **10-Factor Ranking Algorithm**:
  1. Distance (30% weight)
  2. Availability (20%)
  3. Rating (15%)
  4. Review Recency (5%)
  5. Specialization Match (10%)
  6. Price (5%)
  7. Cancellation Rate (5%)
  8. Response Time (5%)
  9. Capacity (3%)
  10. User Preference (2%)
- Returns top 3 providers with scores

#### 3. Pricing Agent
- **Dynamic Pricing Formula**:
  ```
  Final Price = Base Fee 
                + Distance Fee (PKR 10/km)
                + Urgency Surcharge (0-50%)
                + Demand Surge (0-30%)
                - Loyalty Discount (0-15%)
  ```
- Full transparency with breakdown

#### 4. Scheduling Agent
- Checks provider calendar
- Detects conflicts
- Reserves time slot
- Confirms booking

#### 5. Notification Agent
- Multi-channel: SMS, WhatsApp, In-app
- Event-driven: booking_confirmed, en_route, completed
- Simulated for demo

#### 6. Feedback Agent
- Sentiment analysis on reviews
- Rating aggregation
- Reputation updates
- Dispute detection

---

## 🗄️ Database Schema

### 7 Core Tables

1. **users** - Customers, providers, admin
2. **providers** - Provider profiles with location
3. **bookings** - Service bookings with pricing
4. **ai_traces** - AI reasoning logs (for demo)
5. **reviews** - Ratings and feedback
6. **notifications** - Multi-channel notifications
7. **disputes** - Dispute management

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL
- **AI**: Google Gemini 1.5 Flash
- **Maps**: Haversine formula for distance

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State**: Zustand

### Deployment
- **Backend**: Google Cloud Run
- **Frontend**: Vercel
- **Database**: Google Cloud SQL

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Google Gemini API Key

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your credentials
DATABASE_URL=postgresql://user:password@localhost:5432/eshifa
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_secret_key_here

# Run database migrations
psql -U postgres -d eshifa -f ../database/mvp_schema.sql

# Start server
python main.py
```

Backend will run on: `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env.local
cp .env.local.example .env.local

# Edit .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
```

Frontend will run on: `http://localhost:3000`

---

## 🎮 Demo Flow

### User Journey

1. **Landing Page** → Click "Book Service Now"
2. **Service Selection** → Choose from 6 services
3. **Booking Form** → Enter query in any language
4. **AI Processing** → Watch agents work in real-time
5. **Provider Matching** → See top 3 providers with scores
6. **Price Breakdown** → Transparent pricing calculation
7. **Confirmation** → Booking confirmed instantly
8. **Tracking** → Real-time status updates
9. **Feedback** → Rate and review after completion

### Admin View

1. **Dashboard** → Real-time metrics
2. **Live Bookings** → Active bookings monitoring
3. **AI Traces** → View reasoning logs
4. **Provider Performance** → Analytics

---

## 📊 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register user
- `POST /api/auth/login` - Login user

### Bookings
- `POST /api/bookings/create` - Create booking (runs all agents)
- `GET /api/bookings/{id}` - Get booking details with AI traces
- `GET /api/bookings/` - Get user bookings
- `POST /api/bookings/feedback` - Submit feedback

### Admin
- `GET /api/admin/dashboard` - Dashboard metrics
- `GET /api/admin/ai-traces` - Recent AI traces
- `GET /api/admin/bookings/live` - Live bookings
- `GET /api/admin/providers/performance` - Provider analytics

---

## 🎨 Key Features for Demo

### 1. AI Reasoning Visibility
- Every agent logs its reasoning steps
- Visible in booking details page
- Admin dashboard shows live traces
- Execution time tracking

### 2. Multilingual Input
```
English: "I need a home nurse tomorrow at 10 AM"
Urdu: "مجھے کل صبح 10 بجے گھر پر نرس چاہیے"
Roman Urdu: "Mujhe kal subah 10 baje ghar pe nurse chahiye"
```

### 3. Dynamic Pricing Transparency
- Base fee clearly shown
- Distance calculation visible
- Surcharges explained
- Discounts applied
- Final price breakdown

### 4. Provider Matching Intelligence
- 10 factors considered
- Weighted scoring algorithm
- Top 3 providers ranked
- Match score displayed (0-1)

### 5. Real-Time Dashboard
- Auto-refreshes every 5 seconds
- Live booking status
- AI trace logs streaming
- Revenue tracking

---

## 🎯 Hackathon Judging Criteria

### Innovation ✅
- Multi-agent AI orchestration (Antigravity-style)
- 10-factor intelligent matching
- Dynamic pricing algorithm
- Multilingual NLP

### Technical Excellence ✅
- Clean architecture (FastAPI + Next.js)
- PostgreSQL with proper schema
- Google Gemini AI integration
- Real-time updates

### User Experience ✅
- Simple, intuitive flow
- Transparent pricing
- AI reasoning visibility
- Mobile-first design

### Social Impact ✅
- Targets informal economy
- Empowers home healthcare workers
- Accessible in local languages
- Transparent and fair pricing

### Scalability ✅
- Microservices-ready architecture
- Database optimized with indexes
- Stateless API design
- Cloud-native (Google Cloud)

---

## 📈 Sample Data

### Test Users

**Customer**:
- Phone: `+923001234567`
- Password: `password123`
- Role: `customer`

**Provider (Nurse)**:
- Phone: `+923009876543`
- Password: `password123`
- Role: `provider`

**Admin**:
- Phone: `+923005555555`
- Password: `admin123`
- Role: `admin`

---

## 🚀 Deployment

### Backend (Google Cloud Run)

```bash
# Build Docker image
docker build -t eshifa-backend ./backend

# Push to Google Container Registry
docker tag eshifa-backend gcr.io/PROJECT_ID/eshifa-backend
docker push gcr.io/PROJECT_ID/eshifa-backend

# Deploy to Cloud Run
gcloud run deploy eshifa-backend \
  --image gcr.io/PROJECT_ID/eshifa-backend \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated
```

### Frontend (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod
```

---

## 🎥 Demo Script

### 1. Landing Page (30 seconds)
- Show hero section
- Highlight 6 services
- Explain "How It Works"

### 2. Booking Flow (2 minutes)
- Select "Home Nurse"
- Enter multilingual query
- Show AI agents working
- Display provider matching
- Show price breakdown
- Confirm booking

### 3. Booking Details (1 minute)
- Show booking status
- Display AI reasoning traces
- Highlight transparency

### 4. Admin Dashboard (1 minute)
- Show real-time metrics
- Display live bookings
- Show AI trace logs
- Highlight analytics

### 5. Feedback (30 seconds)
- Submit rating
- Show sentiment analysis
- Display reputation update

**Total Demo Time**: 5 minutes

---

## 🏆 Competitive Advantages

1. **True AI Orchestration** - Not just a chatbot, but 6 specialized agents
2. **Transparency** - Every decision explained with reasoning
3. **Fairness** - 10-factor algorithm prevents bias
4. **Accessibility** - Multilingual support for informal economy
5. **Scalability** - Clean architecture ready for growth

---

## 📝 Future Enhancements

- Real WhatsApp/SMS integration
- Google Maps integration
- Payment gateway (Stripe/JazzCash)
- Mobile apps (React Native)
- Voice input/output
- Provider mobile app
- Advanced analytics
- Machine learning for demand prediction

---

## 👥 Team

- **Developer**: [Your Name]
- **Project**: E-Shifa AI
- **Hackathon**: AI Service Orchestrator for Informal Economy
- **Date**: May 2026

---

## 📄 License

Proprietary - All rights reserved

---

## 🙏 Acknowledgments

- Google Gemini AI
- FastAPI Framework
- Next.js Team
- PostgreSQL Community

---

## 📞 Contact

For questions or demo requests:
- Email: contact@eshifa.ai
- GitHub: [Repository Link]
- Demo: [Live Demo URL]

---

**Built with ❤️ for Pakistan's Healthcare Future**

