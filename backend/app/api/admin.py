"""
Admin API - Hackathon MVP
Real-time monitoring and AI trace logs
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from app.core.database import database
from app.core.security import get_current_user

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/dashboard")
async def get_dashboard_metrics(current_user: dict = Depends(get_current_user)):
    """Get real-time dashboard metrics"""
    
    # Total bookings
    total_bookings_query = "SELECT COUNT(*) as count FROM bookings"
    total_bookings = await database.fetch_one(total_bookings_query)
    
    # Active bookings
    active_bookings_query = """
    SELECT COUNT(*) as count FROM bookings 
    WHERE status IN ('confirmed', 'en_route', 'in_progress')
    """
    active_bookings = await database.fetch_one(active_bookings_query)
    
    # Total providers
    total_providers_query = "SELECT COUNT(*) as count FROM providers"
    total_providers = await database.fetch_one(total_providers_query)
    
    # Available providers
    available_providers_query = "SELECT COUNT(*) as count FROM providers WHERE is_available = true"
    available_providers = await database.fetch_one(available_providers_query)
    
    # Total revenue
    revenue_query = "SELECT SUM(final_price) as total FROM bookings WHERE status = 'completed'"
    revenue = await database.fetch_one(revenue_query)
    
    # Service breakdown
    service_breakdown_query = """
    SELECT service_type, COUNT(*) as count 
    FROM bookings 
    GROUP BY service_type
    ORDER BY count DESC
    """
    service_breakdown = await database.fetch_all(service_breakdown_query)
    
    # Average rating
    avg_rating_query = "SELECT AVG(rating) as avg_rating FROM providers"
    avg_rating = await database.fetch_one(avg_rating_query)
    
    return {
        "total_bookings": total_bookings['count'],
        "active_bookings": active_bookings['count'],
        "total_providers": total_providers['count'],
        "available_providers": available_providers['count'],
        "total_revenue": float(revenue['total']) if revenue['total'] else 0,
        "service_breakdown": [dict(s) for s in service_breakdown],
        "average_rating": float(avg_rating['avg_rating']) if avg_rating['avg_rating'] else 0
    }


@router.get("/ai-traces")
async def get_ai_traces(limit: int = 50, current_user: dict = Depends(get_current_user)):
    """Get recent AI reasoning traces"""
    
    query = """
    SELECT 
        t.id,
        t.booking_id,
        t.agent_name,
        t.reasoning_steps,
        t.execution_time_ms,
        t.created_at,
        b.booking_number,
        b.service_type,
        b.status
    FROM ai_traces t
    JOIN bookings b ON t.booking_id = b.id
    ORDER BY t.created_at DESC
    LIMIT :limit
    """
    
    traces = await database.fetch_all(query, {"limit": limit})
    
    return {"traces": [dict(t) for t in traces]}


@router.get("/bookings/live")
async def get_live_bookings(current_user: dict = Depends(get_current_user)):
    """Get live bookings with provider details"""
    
    query = """
    SELECT 
        b.id,
        b.booking_number,
        b.service_type,
        b.status,
        b.urgency,
        b.scheduled_time,
        b.final_price,
        b.created_at,
        u.full_name as customer_name,
        u.phone_number as customer_phone,
        p_user.full_name as provider_name,
        p.rating as provider_rating
    FROM bookings b
    JOIN users u ON b.customer_id = u.id
    LEFT JOIN providers p ON b.provider_id = p.id
    LEFT JOIN users p_user ON p.user_id = p_user.id
    WHERE b.status IN ('confirmed', 'en_route', 'in_progress')
    ORDER BY b.scheduled_time ASC
    """
    
    bookings = await database.fetch_all(query)
    
    return {"live_bookings": [dict(b) for b in bookings]}


@router.get("/providers/performance")
async def get_provider_performance(current_user: dict = Depends(get_current_user)):
    """Get provider performance metrics"""
    
    query = """
    SELECT 
        p.id,
        u.full_name as name,
        p.service_type,
        p.rating,
        p.total_bookings,
        p.cancellation_rate,
        p.is_available,
        COUNT(r.id) as total_reviews,
        AVG(r.sentiment_score) as avg_sentiment
    FROM providers p
    JOIN users u ON p.user_id = u.id
    LEFT JOIN reviews r ON p.id = r.provider_id
    GROUP BY p.id, u.full_name, p.service_type, p.rating, p.total_bookings, p.cancellation_rate, p.is_available
    ORDER BY p.rating DESC
    """
    
    providers = await database.fetch_all(query)
    
    return {"providers": [dict(p) for p in providers]}


@router.get("/analytics/hourly")
async def get_hourly_analytics(current_user: dict = Depends(get_current_user)):
    """Get hourly booking analytics"""
    
    query = """
    SELECT 
        DATE_TRUNC('hour', created_at) as hour,
        COUNT(*) as bookings_count,
        SUM(final_price) as revenue
    FROM bookings
    WHERE created_at >= NOW() - INTERVAL '24 hours'
    GROUP BY hour
    ORDER BY hour DESC
    """
    
    analytics = await database.fetch_all(query)
    
    return {"hourly_analytics": [dict(a) for a in analytics]}
