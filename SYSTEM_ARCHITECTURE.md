# 🏗️ E-Shifa AI - System Architecture

## AI-Powered Home Healthcare Service Orchestrator

---

## 🎯 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                          │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Landing    │  │   Booking    │  │    Admin     │      │
│  │     Page     │  │     Flow     │  │  Dashboard   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│              Next.js 14 + TypeScript + Tailwind              │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST API
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      API GATEWAY                             │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │     Auth     │  │   Bookings   │  │    Admin     │      │
│  │     API      │  │     API      │  │     API      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│                    FastAPI + Python                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   AI AGENT ORCHESTRATOR                      │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Agent 1: Intent Extraction                          │   │
│  │  ↓                                                    │   │
│  │  Agent 2: Provider Matching (10 factors)             │   │
│  │  ↓                                                    │   │
│  │  Agent 3: Dynamic Pricing                            │   │
│  │  ↓                                                    │   │
│  │  Agent 4: Scheduling                                 │   │
│  │  ↓                                                    │   │
│  │  Agent 5: Notifications                              │   │
│  │  ↓                                                    │   │
│  │  Agent 6: Feedback & Reputation                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│              Google Gemini 1.5 Flash API                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                          │
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  users   │  │providers │  │ bookings │  │ai_traces │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ reviews  │  │notifications│ │disputes │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
│                                                               │
│                    PostgreSQL 14+                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🤖 AI Agent Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER REQUEST                              │
│  "Mujhe ghar pe nurse chahiye kal subah 10 baje"           │
│  (I need a home nurse tomorrow at 10 AM)                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  AGENT 1: INTENT EXTRACTION                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  • Detect language: Urdu                               │ │
│  │  • Extract service: home_nurse                         │ │
│  │  • Extract time: tomorrow 10 AM                        │ │
│  │  • Classify urgency: routine                           │ │
│  │  • Confidence: 0.95                                    │ │
│  └────────────────────────────────────────────────────────┘ │
│  Execution: 245ms                                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  AGENT 2: PROVIDER MATCHING                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  10-Factor Algorithm:                                  │ │
│  │  1. Distance: 2.3 km (Score: 0.77)                    │ │
│  │  2. Availability: Yes (Score: 1.00)                   │ │
│  │  3. Rating: 4.8/5 (Score: 0.96)                       │ │
│  │  4. Review Recency: Recent (Score: 0.80)              │ │
│  │  5. Specialization: Match (Score: 0.90)               │ │
│  │  6. Price: PKR 1500 (Score: 0.70)                     │ │
│  │  7. Cancellation: 2% (Score: 0.98)                    │ │
│  │  8. Response Time: 15min (Score: 0.75)                │ │
│  │  9. Capacity: Available (Score: 0.80)                 │ │
│  │  10. Preference: None (Score: 0.70)                   │ │
│  │                                                         │ │
│  │  Weighted Total: 0.92                                  │ │
│  │  Top Provider: Fatima Bibi                             │ │
│  └────────────────────────────────────────────────────────┘ │
│  Execution: 180ms                                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  AGENT 3: DYNAMIC PRICING                                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Base Fee:           PKR 1500                          │ │
│  │  Distance Fee:       PKR 23 (2.3 km × 10)             │ │
│  │  Urgency Surcharge:  PKR 0 (routine = 0%)             │ │
│  │  Demand Surge:       PKR 150 (medium = 10%)           │ │
│  │  Loyalty Discount:   -PKR 76 (silver = 5%)            │ │
│  │  ─────────────────────────────────────────            │ │
│  │  Final Price:        PKR 1597                          │ │
│  └────────────────────────────────────────────────────────┘ │
│  Execution: 120ms                                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  AGENT 4: SCHEDULING                                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  • Check provider calendar                             │ │
│  │  • Detect conflicts: None                              │ │
│  │  • Reserve slot: 2026-05-20 10:00-11:00               │ │
│  │  • Status: Confirmed                                   │ │
│  └────────────────────────────────────────────────────────┘ │
│  Execution: 95ms                                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  AGENT 5: NOTIFICATIONS                                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  SMS: "Booking confirmed! Fatima Bibi will arrive..." │ │
│  │  WhatsApp: "🏥 E-Shifa AI - Booking #ESH12345..."     │ │
│  │  In-App: "Your booking is confirmed"                  │ │
│  └────────────────────────────────────────────────────────┘ │
│  Execution: 150ms                                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  BOOKING CONFIRMED                           │
│  Booking ID: ESH12345678                                     │
│  Provider: Fatima Bibi                                       │
│  Time: May 20, 2026 10:00 AM                                │
│  Price: PKR 1597                                             │
│  Total Processing: 790ms                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Database Schema

```
┌──────────────────────────────────────────────────────────────┐
│                      USERS TABLE                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  id (UUID)                                             │  │
│  │  phone_number (VARCHAR) UNIQUE                         │  │
│  │  full_name (VARCHAR)                                   │  │
│  │  password_hash (VARCHAR)                               │  │
│  │  role (ENUM: customer, provider, admin)                │  │
│  │  loyalty_tier (ENUM: bronze, silver, gold, platinum)   │  │
│  │  created_at (TIMESTAMP)                                │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
                         │
                         │ 1:N
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                    PROVIDERS TABLE                            │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  id (UUID)                                             │  │
│  │  user_id (UUID) FK → users.id                          │  │
│  │  service_type (VARCHAR)                                │  │
│  │  latitude, longitude (DECIMAL)                         │  │
│  │  base_rate (DECIMAL)                                   │  │
│  │  rating (DECIMAL)                                      │  │
│  │  total_bookings (INT)                                  │  │
│  │  cancellation_rate (DECIMAL)                           │  │
│  │  is_available (BOOLEAN)                                │  │
│  │  specialization (TEXT[])                               │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
                         │
                         │ 1:N
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                    BOOKINGS TABLE                             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  id (UUID)                                             │  │
│  │  booking_number (VARCHAR) UNIQUE                       │  │
│  │  customer_id (UUID) FK → users.id                      │  │
│  │  provider_id (UUID) FK → providers.id                  │  │
│  │  service_type (VARCHAR)                                │  │
│  │  status (ENUM)                                         │  │
│  │  urgency (ENUM)                                        │  │
│  │  scheduled_time (TIMESTAMP)                            │  │
│  │  customer_location (JSONB)                             │  │
│  │  distance_km (DECIMAL)                                 │  │
│  │  base_price, distance_fee, urgency_surcharge,         │  │
│  │  demand_surge, loyalty_discount, final_price (DECIMAL) │  │
│  │  user_query (TEXT)                                     │  │
│  │  created_at (TIMESTAMP)                                │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
                         │
                         │ 1:N
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                   AI_TRACES TABLE                             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  id (UUID)                                             │  │
│  │  booking_id (UUID) FK → bookings.id                    │  │
│  │  agent_name (VARCHAR)                                  │  │
│  │  input_data (JSONB)                                    │  │
│  │  reasoning_steps (JSONB)                               │  │
│  │  output_data (JSONB)                                   │  │
│  │  execution_time_ms (INT)                               │  │
│  │  created_at (TIMESTAMP)                                │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

```
┌──────────────┐
│   Customer   │
│   (Browser)  │
└──────┬───────┘
       │
       │ 1. POST /api/bookings/create
       │    {user_query, location}
       ▼
┌──────────────────────────────────────┐
│      FastAPI Backend                 │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  Bookings API                  │ │
│  │  ├─ Validate request           │ │
│  │  ├─ Get user loyalty tier      │ │
│  │  └─ Start AI orchestration     │ │
│  └────────────────────────────────┘ │
└──────┬───────────────────────────────┘
       │
       │ 2. Run AI Agents
       ▼
┌──────────────────────────────────────┐
│   AI Agent Orchestrator              │
│                                      │
│   ┌─────────────────────────────┐   │
│   │ Agent 1: Intent Extraction  │   │
│   │ ↓ Save trace to DB          │   │
│   │ Agent 2: Provider Matching  │   │
│   │ ↓ Save trace to DB          │   │
│   │ Agent 3: Pricing            │   │
│   │ ↓ Save trace to DB          │   │
│   │ Agent 4: Scheduling         │   │
│   │ ↓ Save trace to DB          │   │
│   │ Agent 5: Notifications      │   │
│   │ ↓ Save trace to DB          │   │
│   └─────────────────────────────┘   │
└──────┬───────────────────────────────┘
       │
       │ 3. Save booking & traces
       ▼
┌──────────────────────────────────────┐
│      PostgreSQL Database             │
│                                      │
│  INSERT INTO bookings (...)          │
│  INSERT INTO ai_traces (...)         │
│  UPDATE providers SET ...            │
└──────┬───────────────────────────────┘
       │
       │ 4. Return response
       ▼
┌──────────────────────────────────────┐
│      Customer (Browser)              │
│                                      │
│  {                                   │
│    booking_id,                       │
│    provider,                         │
│    pricing,                          │
│    ai_traces                         │
│  }                                   │
└──────────────────────────────────────┘
```

---

## 🎨 Frontend Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND PAGES                            │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  / (Landing Page)                                     │   │
│  │  ├─ Hero section                                      │   │
│  │  ├─ 6 service cards                                   │   │
│  │  ├─ How it works                                      │   │
│  │  └─ Features showcase                                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  /book (Service Selection)                            │   │
│  │  ├─ 6 service cards                                   │   │
│  │  ├─ Service details                                   │   │
│  │  └─ Booking form                                      │   │
│  │     ├─ User query (multilingual)                      │   │
│  │     ├─ Location input                                 │   │
│  │     ├─ Urgency selector                               │   │
│  │     └─ "Find Provider" button                         │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  /booking/[id] (Booking Details)                      │   │
│  │  ├─ Booking info                                      │   │
│  │  ├─ Provider details                                  │   │
│  │  ├─ Pricing breakdown                                 │   │
│  │  ├─ AI reasoning traces ⭐                            │   │
│  │  └─ Feedback form                                     │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  /admin/dashboard (Admin Panel)                       │   │
│  │  ├─ Real-time metrics                                 │   │
│  │  ├─ Live bookings                                     │   │
│  │  ├─ AI trace logs ⭐                                  │   │
│  │  └─ Provider analytics                                │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│              Next.js 14 + TypeScript + Tailwind              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      PRODUCTION                              │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Vercel (Frontend)                        │   │
│  │  ├─ Next.js SSR                                       │   │
│  │  ├─ Edge Functions                                    │   │
│  │  └─ CDN Distribution                                  │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                      │
│                       │ HTTPS                                │
│                       ▼                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Google Cloud Run (Backend)                    │   │
│  │  ├─ FastAPI Container                                 │   │
│  │  ├─ Auto-scaling                                      │   │
│  │  └─ Load Balancing                                    │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                      │
│                       │                                      │
│                       ▼                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │       Google Cloud SQL (PostgreSQL)                   │   │
│  │  ├─ Managed Database                                  │   │
│  │  ├─ Automatic Backups                                 │   │
│  │  └─ High Availability                                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Google Gemini API                             │   │
│  │  └─ AI Model Inference                                │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                           │
│                                                               │
│  Layer 1: Authentication                                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  • JWT Token (HS256)                                   │ │
│  │  • Bcrypt Password Hashing                             │ │
│  │  • 24-hour Token Expiration                            │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
│  Layer 2: Authorization                                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  • Role-Based Access Control (RBAC)                    │ │
│  │  • Endpoint Protection                                 │ │
│  │  • User Ownership Validation                           │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
│  Layer 3: Data Protection                                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  • SQL Injection Prevention (Parameterized Queries)    │ │
│  │  • XSS Protection (Input Sanitization)                 │ │
│  │  • CORS Configuration                                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
│  Layer 4: Database Security                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  • Foreign Key Constraints                             │ │
│  │  • Cascade Delete Rules                                │ │
│  │  • Encrypted Connections                               │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

**Built with ❤️ for Pakistan's Healthcare Future**

