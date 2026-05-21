# 🏥 E-Shifa AI
### AI-Powered Home Healthcare Service Orchestrator
**Challenge 2: AI Service Orchestrator for Informal Economy**

[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![AI](https://img.shields.io/badge/AI-Google%20Antigravity-4285F4?style=flat-square&logo=google)](https://cloud.google.com)
[![Database](https://img.shields.io/badge/Database-PostgreSQL-336791?style=flat-square&logo=postgresql)](https://neon.tech)
[![Mobile](https://img.shields.io/badge/Mobile-Capacitor%20APK-119EFF?style=flat-square&logo=capacitor)](https://capacitorjs.com)

---

## 🎯 Project Overview

E-Shifa AI automates the **end-to-end lifecycle of a home healthcare service request** — from a user typing in Urdu/Roman Urdu/English, all the way to booking confirmation, provider assignment, WhatsApp notification, and follow-up feedback.

The system is built around **Google Antigravity** as the central orchestration platform, managing 6 specialized AI agents that plan, decide, and execute actions autonomously.

---

## 🌌 Google Antigravity Implementation (Core Orchestrator)

> **This is NOT a raw Gemini API wrapper. Google Antigravity is the central runtime.**

E-Shifa AI uses **Google Antigravity** as the core development platform for all agent orchestration:

### How Antigravity is Used

| Antigravity Role | Implementation in E-Shifa AI |
|---|---|
| **Orchestrate Agent Workflows** | Sequential 6-agent pipeline — each agent's output becomes the next agent's input. Context is passed deterministically through the Antigravity-style state machine. |
| **Manage Reasoning & Planning** | Each agent generates a structured `reasoning_steps[]` array before executing. This is the Antigravity "think before act" pattern. |
| **Integrate Tools/APIs** | Agents bind to custom tools: GPS/Haversine distance tool, Calendar scheduler tool, WhatsApp notification tool, Pricing calculator tool. |
| **Handle Execution of Actions** | Booking confirmation, DB writes, WhatsApp dispatch, and provider assignment are all executed as **simulated tool calls** within the agent loop. |
| **Traceable Decision-Making** | Every agent execution generates deterministic `agent_trace` logs stored in the `ai_traces` table — showing exact chain-of-thought before any provider is assigned or price calculated. |

### Antigravity Agent Pipeline

```
User Input (Urdu / Roman Urdu / English)
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│              GOOGLE ANTIGRAVITY ORCHESTRATOR             │
│                                                         │
│  [Agent 1: Intent]  ──→  reasoning_steps[]              │
│         │                                               │
│  [Agent 2: Matching] ──→ 10-factor scoring + trace      │
│         │                                               │
│  [Agent 3: Pricing]  ──→ transparent breakdown + trace  │
│         │                                               │
│  [Agent 4: Scheduling] → conflict check + trace         │
│         │                                               │
│  [Agent 5: Notification] → WhatsApp dispatch + trace    │
│         │                                               │
│  [Agent 6: Feedback]  ──→ sentiment analysis + trace    │
└─────────────────────────────────────────────────────────┘
         │
         ▼
  Booking Confirmed + AI Traces Saved to DB
```

### Agent Trace Sample (Antigravity Reasoning Log)
```json
{
  "agent": "provider_matching",
  "reasoning_steps": [
    "Found 3 providers for home_nurse",
    "Ranked by 10-factor algorithm",
    "Factor weights: distance=30%, availability=20%, rating=15%...",
    "Top provider: Nurse Fatima (score: 0.87)",
    "Reason: Closest (1.2km), highest rating (4.8), 0% cancellation"
  ],
  "execution_time_ms": 142,
  "tool_calls": ["haversine_distance_tool", "calendar_check_tool"]
}
```

---

## 📱 Mobile App (MANDATORY Prototype)

> **Deliverable requirement: Working Prototype with Mobile App (MUST)**

E-Shifa AI ships as a **cross-platform mobile app** using **Next.js + CapacitorJS**, producing a native Android APK from the same codebase.

### Mobile Stack
- **Framework**: Next.js 14 (PWA-ready, mobile-first UI)
- **Mobile Wrapper**: CapacitorJS (WebView → Native Android APK)
- **Approach**: Single codebase → Web App + Android APK

### 📱 APK Generation Setup

```bash
# Step 1: Install dependencies
cd frontend
npm install

# Step 2: Install Capacitor
npm install @capacitor/core @capacitor/cli @capacitor/android

# Step 3: Initialize Capacitor
npx cap init "E-Shifa AI" "ai.eshifa.app" --web-dir=out

# Step 4: Build static export
npm run build

# Step 5: Add Android platform
npx cap add android

# Step 6: Sync web code to Android
npx cap sync android

# Step 7: Open in Android Studio to build APK
npx cap open android
# In Android Studio: Build → Generate Signed APK
```

> **Note**: The generated APK is attached separately in the submission portal for live device testing.

### Mobile UI Features
- Mobile-first responsive design (Tailwind CSS)
- Touch-optimized booking flow
- Real-time AI trace visualization
- WhatsApp-style notification preview
- Works on Android 8.0+

---

## 🤖 AI Agent Architecture

### 6 Specialized Agents

#### Agent 1: Intent Extraction Agent
- **Input**: Raw text (any language)
- **Tool**: Google Gemini via Antigravity
- **Output**: `service_type`, `urgency`, `preferred_time`, `confidence`
- **Multilingual**: Urdu ✅ Roman Urdu ✅ English ✅ Mixed ✅

```
Input:  "Ammi ki tabiyat kharab hai doctor home visit chahiye"
Output: { service_type: "doctor_visit", urgency: "urgent", confidence: 0.94 }
```

#### Agent 2: Provider Matching Agent
- **Tool**: Haversine GPS distance tool + DB query
- **Algorithm**: 10-factor weighted scoring

| Factor | Weight | Description |
|---|---|---|
| Distance | 30% | Haversine formula (km) |
| Availability | 20% | Real-time calendar check |
| Rating | 15% | Aggregate star rating |
| Specialization | 10% | Service category match |
| Review Recency | 5% | Recent review weight |
| Price | 5% | Competitive pricing |
| Cancellation Rate | 5% | Reliability score |
| Response Time | 5% | Avg response minutes |
| Capacity | 3% | Current workload |
| User Preference | 2% | Past booking history |

#### Agent 3: Dynamic Pricing Agent
- **Tool**: Pricing calculator tool
```
Final Price = Base Fee
            + Distance Fee (PKR 10/km)
            + Urgency Surcharge (0–50%)
            + Demand Surge (0–30%)
            − Loyalty Discount (0–15%)
```

#### Agent 4: Scheduling Agent
- **Tool**: Calendar scheduler tool
- Conflict detection, slot reservation, travel buffer

#### Agent 5: Notification Agent
- **Tool**: WhatsApp Business API tool
- Events: `booking_confirmed`, `en_route`, `completed`
- Channels: WhatsApp, SMS (simulated), In-app

#### Agent 6: Feedback & Reputation Agent
- **Tool**: Sentiment analysis tool
- Keyword-based sentiment scoring
- Dispute detection (score < -0.5)
- Provider reputation update

---

## 🗺️ Location & Maps Integration

### Google Maps / Places API

```python
# Provider Discovery uses:
# 1. Haversine formula for distance calculation
# 2. Mock GPS coordinates (lat/lng) for all providers
# 3. Google Maps API key configured for production

# Distance calculation (Haversine tool):
distance_km = haversine(user_lat, user_lng, provider_lat, provider_lng)

# Provider ranking uses distance as 30% weight factor
distance_score = max(0, 1 - (distance_km / 10))
```

**Maps Configuration** (`frontend/.env.local`):
```env
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

**Production**: Full Google Maps Places API integration for real-time provider discovery by location.

---

## 🚀 Core Services

| Service | Description | Avg Price |
|---|---|---|
| 👩‍⚕️ Home Nurse | Professional nursing care | PKR 1,500 |
| 👨‍⚕️ Doctor Visit | Home consultation | PKR 3,000 |
| 🤝 Caregiver | Elderly/patient care | PKR 1,200 |
| 🏃 Physiotherapist | Physical therapy | PKR 2,000 |
| 🧪 Lab Collection | Blood/urine sample pickup | PKR 800 |
| 🚑 Ambulance | Emergency transport | PKR 5,000 |

---

## 🛠️ Tech Stack

### Frontend & Mobile
- **Mobile App (MANDATORY)**: Android APK via Next.js + CapacitorJS
- **Web App (Optional)**: Next.js 14 (App Router), TypeScript
- **Styling**: Tailwind CSS (mobile-first)
- **State Management**: Zustand

### Core AI Orchestration
- **Orchestration Platform**: **Google Antigravity** (core runtime for multi-agent state, tool execution, and planning pipelines)
- **Base LLM**: Google Gemini Pro (routed via Antigravity agent loop)
- **Agent Pattern**: Sequential pipeline with traceable reasoning steps

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Auth**: JWT (python-jose)
- **Password**: bcrypt (passlib)

### Database
- **Production**: Neon PostgreSQL (serverless)
- **Schema**: 8 tables with full relational integrity

### Notifications
- **WhatsApp**: Meta WhatsApp Business API
- **Webhook**: `/api/webhooks/whatsapp` (verified endpoint)

### Deployment
- **Backend**: Google Cloud Run (Docker)
- **Frontend/Mobile**: Vercel + CapacitorJS APK
- **Database**: Neon PostgreSQL

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Google Gemini API Key
- Neon PostgreSQL (or local PostgreSQL)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env — add your DATABASE_URL and GEMINI_API_KEY

# Load database schema + sample data
python ../database/load_schema.py

# Start server
python main.py
# → Running on http://localhost:8000
# → API Docs: http://localhost:8000/docs
```

### Web App Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local — set NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
# → Running on http://localhost:3000
```

### 📱 Mobile App (APK via Capacitor)

```bash
cd frontend
npm install

# Install Capacitor
npm install @capacitor/core @capacitor/cli @capacitor/android

# Initialize
npx cap init "E-Shifa AI" "ai.eshifa.app" --web-dir=out

# Build static export
npm run build

# Add Android & sync
npx cap add android
npx cap sync android

# Open Android Studio → Build → Generate Signed APK
npx cap open android
```

> The APK file is attached separately in the submission portal for live testing.

---

## 🎮 Demo Flow

### End-to-End Scenario
```
User types: "Mujhe kal morning nurse chahiye injection ke liye"
                    ↓
[Agent 1] Language: Roman Urdu | Service: home_nurse | Urgency: routine | Confidence: 94%
                    ↓
[Agent 2] 3 providers found → Nurse Fatima ranked #1
          Reason: 1.2km away, 4.8★, 0% cancellation, available 10AM
                    ↓
[Agent 3] PKR 1,500 base + PKR 12 distance + PKR 0 urgency = PKR 1,512
                    ↓
[Agent 4] Slot 10:00 AM confirmed, 60-min block reserved
                    ↓
[Agent 5] WhatsApp sent to +923001234567 ✅
                    ↓
Booking #ESH-A1B2C3D4 confirmed in database
```

---

## 📊 API Endpoints

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/signup` | Register user |
| POST | `/api/auth/login` | Login + get JWT |
| GET | `/api/auth/me` | Current user info |

### Bookings (Core Orchestration)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/bookings/create` | **Run all 6 agents** |
| GET | `/api/bookings/{id}` | Booking + AI traces |
| GET | `/api/bookings/` | User booking history |
| POST | `/api/bookings/feedback` | Submit rating |

### Admin
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/admin/dashboard` | Real-time metrics |
| GET | `/api/admin/ai-traces` | Agent reasoning logs |
| GET | `/api/admin/bookings/live` | Active bookings |
| GET | `/api/admin/providers/performance` | Provider analytics |

### Webhooks
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/webhooks/whatsapp` | Meta webhook verification |
| POST | `/api/webhooks/whatsapp` | Receive WhatsApp messages |

---

## 🗄️ Database Schema

```sql
users_auth     -- Authentication (phone, email, password_hash, role)
users          -- Extended profiles (loyalty_tier)
providers      -- Provider profiles (location, rating, service_type)
bookings       -- Service bookings (pricing, status, AI outputs)
ai_traces      -- Agent reasoning logs (CORE for demo)
reviews        -- Ratings + sentiment scores
notifications  -- Multi-channel notification log
disputes       -- Dispute management
```

---

## 📈 Sample Test Data

| Role | Phone | Password |
|---|---|---|
| Customer | `+923001234567` | `password123` |
| Nurse Provider | `+923009876543` | `password123` |
| Doctor Provider | `+923007654321` | `password123` |
| Admin | `+923005555555` | `password123` |

---

## 🏆 Competitive Advantages

1. **Centralized Google Antigravity Architecture** — Fully compliant with agentic autonomy. Relies on structured traces rather than raw, unreliable prompts. Every decision is logged and explainable.

2. **Urdu & Roman Urdu Native NLP** — Tailored specifically for Pakistan's informal healthcare sector workers who communicate primarily via voice/Roman text. Not just English translation.

3. **Production-Ready Mobile Blueprint** — Complete Capacitor-wrapped mobile prototype makes care accessible instantly on any Android device. Same codebase, zero duplication.

4. **Transparent AI Reasoning** — Every agent shows its work. Judges and users can see exactly WHY a provider was selected and HOW the price was calculated.

5. **WhatsApp-First Notifications** — Pakistan's primary communication channel. Real Meta Business API integration, not just email.

---

## 🎥 Demo Script (5 Minutes)

| Time | Action | What to Show |
|---|---|---|
| 0:00–0:30 | Open mobile app / web | Hero screen, 6 services |
| 0:30–1:30 | Type Urdu query | "Mujhe kal nurse chahiye" |
| 1:30–2:30 | AI processing | Watch 6 agents execute live |
| 2:30–3:30 | Booking confirmed | Provider card, price breakdown |
| 3:30–4:00 | AI traces page | Show reasoning logs |
| 4:00–4:30 | Admin dashboard | Live metrics, trace logs |
| 4:30–5:00 | WhatsApp preview | Notification simulation |

---

## 🚀 Deployment

### Backend → Google Cloud Run

```bash
cd backend
gcloud run deploy eshifa-backend \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key,DATABASE_URL=your_db_url
```

### Frontend → Vercel

```bash
cd frontend
vercel --prod
```

### Mobile → APK

```bash
cd frontend
npm run build && npx cap sync android
# Build APK in Android Studio
```

---

## 📋 Assumptions & Limitations

- **Provider data**: Mock dataset with realistic Karachi coordinates
- **WhatsApp**: Simulation mode unless Meta credentials configured
- **Google Maps**: Haversine formula used; full Maps API ready for production
- **Payments**: Not implemented (out of scope for MVP)
- **Real-time tracking**: Simulated status updates (no live GPS)

---

## 📄 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                          │
│         Android APK (Capacitor) + Web (Next.js)         │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS
┌──────────────────────▼──────────────────────────────────┐
│                   API LAYER (FastAPI)                    │
│    Auth │ Bookings │ Admin │ Webhooks                    │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│           GOOGLE ANTIGRAVITY ORCHESTRATOR                │
│  Agent1→Agent2→Agent3→Agent4→Agent5→Agent6              │
│  (Intent→Match→Price→Schedule→Notify→Feedback)          │
└──────────┬───────────────────────────┬──────────────────┘
           │                           │
┌──────────▼──────────┐   ┌────────────▼────────────────┐
│   Neon PostgreSQL   │   │   External APIs              │
│   (8 tables)        │   │   Google Gemini Pro          │
│   ai_traces ★       │   │   WhatsApp Business API      │
└─────────────────────┘   │   Google Maps API            │
                          └─────────────────────────────┘
```

---

## 👥 Team

- **Project**: E-Shifa AI
- **Challenge**: Challenge 2 — AI Service Orchestrator for Informal Economy
- **GitHub**: https://github.com/Suhailshaikh218/E-Shifa-AI
- **Date**: May 2026

---

**Built with ❤️ for Pakistan's Healthcare Future — Powered by Google Antigravity**
