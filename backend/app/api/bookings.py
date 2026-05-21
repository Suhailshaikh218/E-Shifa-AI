"""
Booking API - Hackathon MVP
Main orchestration endpoint
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
from pydantic import BaseModel
from datetime import datetime
import uuid
from app.core.database import database
from app.core.security import get_current_user
from app.services.ai_agents import (
    IntentExtractionAgent,
    ProviderMatchingAgent,
    PricingAgent,
    SchedulingAgent,
    NotificationAgent,
    FeedbackAgent
)

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])


# Schemas
class BookingRequest(BaseModel):
    user_query: str
    location: Dict[str, Any]  # {lat, lng, address}


class ProviderSelectionRequest(BaseModel):
    booking_id: str
    provider_id: str


class FeedbackRequest(BaseModel):
    booking_id: str
    rating: int
    comment: str


# ============================================
# 1. CREATE BOOKING (Full AI Orchestration)
# ============================================
@router.post("/create")
async def create_booking(request: BookingRequest, current_user: dict = Depends(get_current_user)):
    """
    Main orchestration endpoint - runs all AI agents
    """
    try:
        booking_id = str(uuid.uuid4())
        booking_number = f"ESH{str(uuid.uuid4())[:8].upper()}"
        
        # Get user loyalty tier
        user_query = """
        SELECT u.loyalty_tier FROM users u WHERE u.id = :user_id
        """
        user_data = await database.fetch_one(user_query, {"user_id": current_user["user_id"]})
        loyalty_tier = user_data['loyalty_tier'] if user_data else 'bronze'
        
        # ============================================
        # AGENT 1: Intent Extraction
        # ============================================
        intent_result = await IntentExtractionAgent.extract(
            request.user_query,
            request.location
        )
        
        intent_output = intent_result['output']
        
        # Save AI trace
        await save_ai_trace(
            booking_id,
            "intent_extraction",
            {"user_query": request.user_query, "location": request.location},
            intent_result['reasoning'],
            intent_output,
            intent_result['execution_time_ms']
        )
        
        # ============================================
        # AGENT 2: Provider Matching
        # ============================================
        # Fetch available providers
        providers_query = """
        SELECT p.id, ua.full_name as name, p.latitude, p.longitude, p.base_rate, 
               p.rating, p.total_bookings, p.cancellation_rate, p.is_available,
               p.specialization, p.response_time_avg_minutes
        FROM providers p
        JOIN users_auth ua ON p.user_id = ua.id
        WHERE p.service_type = :service_type AND p.is_available = true
        """
        providers = await database.fetch_all(
            providers_query,
            {"service_type": intent_output['service_type']}
        )
        
        if not providers:
            raise HTTPException(
                status_code=404,
                detail=f"No providers available for {intent_output['service_type']}"
            )
        
        providers_list = [dict(p) for p in providers]
        
        matching_result = await ProviderMatchingAgent.match(
            intent_output['service_type'],
            request.location,
            intent_output['urgency'],
            providers_list
        )
        
        # Save AI trace
        await save_ai_trace(
            booking_id,
            "provider_matching",
            {"service_type": intent_output['service_type'], "location": request.location},
            matching_result['reasoning'],
            matching_result['output'],
            matching_result['execution_time_ms']
        )
        
        # Get top provider
        top_provider = matching_result['output']['matched_providers'][0]
        
        # ============================================
        # AGENT 3: Pricing
        # ============================================
        pricing_result = await PricingAgent.calculate(
            base_rate=top_provider['base_rate'],
            distance_km=top_provider['distance_km'],
            urgency=intent_output['urgency'],
            demand_level="medium",  # Simplified
            loyalty_tier=loyalty_tier
        )
        
        # Save AI trace
        await save_ai_trace(
            booking_id,
            "pricing",
            {"base_rate": top_provider['base_rate'], "distance_km": top_provider['distance_km']},
            pricing_result['reasoning'],
            pricing_result['output'],
            pricing_result['execution_time_ms']
        )
        
        pricing_output = pricing_result['output']
        
        # ============================================
        # AGENT 4: Scheduling
        # ============================================
        scheduling_result = await SchedulingAgent.schedule(
            provider_id=top_provider['provider_id'],
            preferred_time=intent_output['preferred_time']
        )
        
        # Save AI trace
        await save_ai_trace(
            booking_id,
            "scheduling",
            {"provider_id": top_provider['provider_id'], "preferred_time": intent_output['preferred_time']},
            scheduling_result['reasoning'],
            scheduling_result['output'],
            scheduling_result['execution_time_ms']
        )
        
        # ============================================
        # Create Booking Record
        # ============================================
        insert_query = """
        INSERT INTO bookings (
            id, booking_number, customer_id, provider_id, service_type,
            status, urgency, scheduled_time, customer_location, distance_km,
            base_price, distance_fee, urgency_surcharge, demand_surge,
            loyalty_discount, final_price, user_query
        ) VALUES (
            :id, :booking_number, :customer_id, :provider_id, :service_type,
            :status, :urgency, :scheduled_time, :customer_location, :distance_km,
            :base_price, :distance_fee, :urgency_surcharge, :demand_surge,
            :loyalty_discount, :final_price, :user_query
        )
        """
        
        await database.execute(insert_query, {
            "id": booking_id,
            "booking_number": booking_number,
            "customer_id": current_user["user_id"],
            "provider_id": top_provider['provider_id'],
            "service_type": intent_output['service_type'],
            "status": "confirmed",
            "urgency": intent_output['urgency'],
            "scheduled_time": intent_output['preferred_time'],
            "customer_location": request.location,
            "distance_km": top_provider['distance_km'],
            "base_price": pricing_output['base_fee'],
            "distance_fee": pricing_output['distance_fee'],
            "urgency_surcharge": pricing_output['urgency_surcharge'],
            "demand_surge": pricing_output['demand_surge'],
            "loyalty_discount": pricing_output['loyalty_discount'],
            "final_price": pricing_output['final_price'],
            "user_query": request.user_query
        })
        
        # ============================================
        # AGENT 5: Notifications
        # ============================================
        # Get customer details
        customer_query = """
        SELECT full_name, phone_number FROM users_auth WHERE id = :user_id
        """
        customer_data = await database.fetch_one(customer_query, {"user_id": current_user["user_id"]})
        
        notification_result = await NotificationAgent.send(
            booking_id=booking_id,
            customer_phone=customer_data['phone_number'] if customer_data else "+92300000000",
            provider_name=top_provider['name'],
            scheduled_time=intent_output['preferred_time'],
            event_type="booking_confirmed",
            customer_name=customer_data['full_name'] if customer_data else "Customer",
            service_type=intent_output['service_type'],
            booking_number=booking_number,
            final_price=pricing_output['final_price']
        )
        
        # Save AI trace
        await save_ai_trace(
            booking_id,
            "notification",
            {"event_type": "booking_confirmed"},
            notification_result['reasoning'],
            notification_result['output'],
            notification_result['execution_time_ms']
        )
        
        return {
            "success": True,
            "booking_id": booking_id,
            "booking_number": booking_number,
            "provider": top_provider,
            "pricing": pricing_output,
            "scheduled_time": intent_output['preferred_time'],
            "all_matched_providers": matching_result['output']['matched_providers'],
            "ai_traces": {
                "intent_extraction": intent_result['reasoning'],
                "provider_matching": matching_result['reasoning'],
                "pricing": pricing_result['reasoning'],
                "scheduling": scheduling_result['reasoning'],
                "notification": notification_result['reasoning']
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# 2. GET BOOKING DETAILS
# ============================================
@router.get("/{booking_id}")
async def get_booking(booking_id: str, current_user: dict = Depends(get_current_user)):
    """Get booking details with AI traces"""
    query = """
    SELECT b.*, ua.full_name as provider_name, ua.phone_number as provider_phone
    FROM bookings b
    LEFT JOIN providers p ON b.provider_id = p.id
    LEFT JOIN users_auth ua ON p.user_id = ua.id
    WHERE b.id = :booking_id
    """
    
    booking = await database.fetch_one(query, {"booking_id": booking_id})
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Get AI traces
    traces_query = """
    SELECT agent_name, reasoning_steps, execution_time_ms, created_at
    FROM ai_traces
    WHERE booking_id = :booking_id
    ORDER BY created_at ASC
    """
    
    traces = await database.fetch_all(traces_query, {"booking_id": booking_id})
    
    return {
        "booking": dict(booking),
        "ai_traces": [dict(t) for t in traces]
    }


# ============================================
# 3. GET USER BOOKINGS
# ============================================
@router.get("/")
async def get_user_bookings(current_user: dict = Depends(get_current_user)):
    """Get all bookings for current user"""
    query = """
    SELECT b.*, ua.full_name as provider_name
    FROM bookings b
    LEFT JOIN providers p ON b.provider_id = p.id
    LEFT JOIN users_auth ua ON p.user_id = ua.id
    WHERE b.customer_id = :user_id
    ORDER BY b.created_at DESC
    """
    
    bookings = await database.fetch_all(query, {"user_id": current_user["user_id"]})
    
    return {"bookings": [dict(b) for b in bookings]}


# ============================================
# 4. SUBMIT FEEDBACK
# ============================================
@router.post("/feedback")
async def submit_feedback(request: FeedbackRequest, current_user: dict = Depends(get_current_user)):
    """Submit feedback and rating"""
    
    # Get booking details
    booking_query = """
    SELECT provider_id FROM bookings WHERE id = :booking_id
    """
    booking = await database.fetch_one(booking_query, {"booking_id": request.booking_id})
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Process feedback with AI
    feedback_result = await FeedbackAgent.process(request.rating, request.comment)
    
    # Save review
    review_id = str(uuid.uuid4())
    insert_review = """
    INSERT INTO reviews (id, booking_id, customer_id, provider_id, rating, comment, sentiment_score)
    VALUES (:id, :booking_id, :customer_id, :provider_id, :rating, :comment, :sentiment_score)
    """
    
    await database.execute(insert_review, {
        "id": review_id,
        "booking_id": request.booking_id,
        "customer_id": current_user["user_id"],
        "provider_id": booking['provider_id'],
        "rating": request.rating,
        "comment": request.comment,
        "sentiment_score": feedback_result['output']['sentiment_score']
    })
    
    # Update provider rating
    update_rating = """
    UPDATE providers
    SET rating = (
        SELECT AVG(rating) FROM reviews WHERE provider_id = :provider_id
    ),
    total_bookings = total_bookings + 1
    WHERE id = :provider_id
    """
    
    await database.execute(update_rating, {"provider_id": booking['provider_id']})
    
    # Save AI trace
    await save_ai_trace(
        request.booking_id,
        "feedback",
        {"rating": request.rating, "comment": request.comment},
        feedback_result['reasoning'],
        feedback_result['output'],
        feedback_result['execution_time_ms']
    )
    
    return {
        "success": True,
        "sentiment": feedback_result['output'],
        "reasoning": feedback_result['reasoning']
    }


# ============================================
# Helper Functions
# ============================================
async def save_ai_trace(booking_id: str, agent_name: str, input_data: dict, reasoning: list, output_data: dict, execution_time: int):
    """Save AI reasoning trace to database"""
    query = """
    INSERT INTO ai_traces (id, booking_id, agent_name, input_data, reasoning_steps, output_data, execution_time_ms)
    VALUES (:id, :booking_id, :agent_name, :input_data, :reasoning_steps, :output_data, :execution_time_ms)
    """
    
    await database.execute(query, {
        "id": str(uuid.uuid4()),
        "booking_id": booking_id,
        "agent_name": agent_name,
        "input_data": input_data,
        "reasoning_steps": reasoning,
        "output_data": output_data,
        "execution_time_ms": execution_time
    })
