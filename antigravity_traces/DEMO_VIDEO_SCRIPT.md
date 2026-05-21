# 🎬 Demo Video Script — E-Shifa AI
## Challenge 2: AI Service Orchestrator for Informal Economy

---

## Video 1: Main Demo (3-5 minutes)

### Scene 1: Introduction (0:00 - 0:30)
**Show**: Project homepage / README on GitHub
**Say**: 
> "E-Shifa AI is an AI-powered home healthcare service orchestrator for Pakistan's informal economy. It uses Google Antigravity to orchestrate 6 AI agents that handle everything from understanding your Urdu request to booking a nurse and sending a WhatsApp confirmation."

---

### Scene 2: Backend API Docs (0:30 - 1:00)
**Show**: Open http://localhost:8000/docs
**Say**:
> "Here's our FastAPI backend with all endpoints. The core endpoint is POST /api/bookings/create — this triggers the entire Antigravity agent pipeline."

---

### Scene 3: User Registration (1:00 - 1:30)
**Show**: POST /api/auth/signup in Swagger UI
**Input**:
```json
{
  "full_name": "Ahmed Khan",
  "phone_number": "+923001111111",
  "email": "ahmed@test.com",
  "password": "password123",
  "role": "customer"
}
```
**Say**: "First, a user registers. They get a JWT token back."

---

### Scene 4: Create Booking — AI Orchestration (1:30 - 3:00)
**Show**: POST /api/bookings/create
**Input**:
```json
{
  "user_query": "Mujhe kal morning nurse chahiye injection ke liye",
  "location": {
    "lat": 24.8607,
    "lng": 67.0011,
    "address": "Karachi, Pakistan"
  }
}
```
**Say**:
> "Watch what happens when I submit this Roman Urdu query. All 6 Antigravity agents execute in sequence."

**Show response — highlight**:
- `ai_traces.intent_extraction` → language detected, service extracted
- `ai_traces.provider_matching` → 10-factor scoring, top provider selected
- `ai_traces.pricing` → transparent price breakdown
- `ai_traces.scheduling` → slot confirmed
- `ai_traces.notification` → WhatsApp sent

---

### Scene 5: View AI Traces (3:00 - 4:00)
**Show**: GET /api/admin/ai-traces
**Say**:
> "Every agent's reasoning is stored in our database. This is the Antigravity trace log — showing exactly how each decision was made."

---

### Scene 6: Admin Dashboard (4:00 - 4:30)
**Show**: GET /api/admin/dashboard
**Say**:
> "The admin dashboard shows real-time metrics — total bookings, active providers, revenue, and service breakdown."

---

### Scene 7: Wrap Up (4:30 - 5:00)
**Show**: GitHub repo README
**Say**:
> "E-Shifa AI is fully deployed on GitHub, with complete documentation, WhatsApp integration, and a mobile APK via CapacitorJS. Built for Pakistan's informal healthcare economy."

---

## Video 2: Antigravity Usage (2-3 minutes)

### Scene 1: Show ai_agents.py (0:00 - 0:45)
**Show**: Open `backend/app/services/ai_agents.py`
**Say**:
> "This is our core Antigravity implementation. Each class is an agent. Each agent follows the Antigravity pattern: Plan → Execute → Trace."

**Highlight**:
```python
reasoning = [
    f"Language detected: {result['language']}",
    f"Service identified: {result['service_type']}",
    f"Confidence score: {result['confidence']}"
]
return {
    "output": result,
    "reasoning": reasoning,      # ← Antigravity trace
    "execution_time_ms": elapsed
}
```

---

### Scene 2: Show bookings.py Pipeline (0:45 - 1:30)
**Show**: Open `backend/app/api/bookings.py`
**Say**:
> "In bookings.py, you can see the Antigravity orchestration pipeline. Agent 1 output feeds into Agent 2, which feeds into Agent 3, and so on. Each step saves its trace to the database."

**Highlight the sequential calls**:
```python
intent_result = await IntentExtractionAgent.extract(...)
matching_result = await ProviderMatchingAgent.match(...)
pricing_result = await PricingAgent.calculate(...)
scheduling_result = await SchedulingAgent.schedule(...)
notification_result = await NotificationAgent.send(...)
```

---

### Scene 3: Live API Call + Trace (1:30 - 2:30)
**Show**: Make a live booking via Swagger UI
**Show**: The response with full `ai_traces` object
**Say**:
> "Here you can see the complete Antigravity trace. Each agent shows its reasoning steps, what tools it called, and how long it took. This is full agentic transparency."

---

### Scene 4: Database Traces (2:30 - 3:00)
**Show**: GET /api/admin/ai-traces response
**Say**:
> "All traces are persisted in PostgreSQL. This is the Antigravity execution log — workplan, task list, reasoning steps, and action execution — all stored and queryable."

---

## 📝 Recording Tips

1. Use OBS Studio or Loom for screen recording
2. Show terminal with backend running (logs visible)
3. Use Swagger UI at http://localhost:8000/docs
4. Zoom in on JSON responses to make them readable
5. Keep it under 5 minutes for Demo, 3 minutes for Antigravity
6. Add captions if possible

---

## 🎯 Key Points to Emphasize

- "Google Antigravity is the CORE orchestrator — not just a Gemini wrapper"
- "6 agents work sequentially — each one's output is the next one's input"
- "Every decision is traceable — stored in ai_traces table"
- "Multilingual: Urdu, Roman Urdu, English all work"
- "WhatsApp notification sent automatically after booking"
- "10-factor provider matching — not just distance"
