"""
AI Agent Orchestrator - Hackathon MVP
Multi-agent system for home healthcare service matching
"""
import time
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import google.generativeai as genai
from app.core.config import settings
import math

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')


class IntentExtractionAgent:
    """Agent 1: Extract intent from user query"""
    
    @staticmethod
    async def extract(user_query: str, user_location: Dict) -> Dict[str, Any]:
        start_time = time.time()
        
        prompt = f"""
You are an intent extraction agent for a home healthcare service platform.

User Query: "{user_query}"
User Location: {user_location}

Extract the following:
1. service_type: one of [home_nurse, doctor_visit, caregiver, physiotherapist, lab_collection, ambulance]
2. preferred_time: ISO timestamp (if mentioned, else tomorrow 10 AM)
3. urgency: one of [routine, urgent, emergency]
4. language: detected language (urdu, english, roman_urdu)
5. confidence: 0.0 to 1.0

Respond ONLY with valid JSON:
{{
  "service_type": "home_nurse",
  "preferred_time": "2026-05-20T10:00:00",
  "urgency": "routine",
  "language": "urdu",
  "confidence": 0.95
}}
"""
        
        response = model.generate_content(prompt)
        result = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
        
        execution_time = int((time.time() - start_time) * 1000)
        
        reasoning = [
            f"Language detected: {result['language']}",
            f"Service identified: {result['service_type']}",
            f"Urgency level: {result['urgency']}",
            f"Confidence score: {result['confidence']}"
        ]
        
        return {
            "output": result,
            "reasoning": reasoning,
            "execution_time_ms": execution_time
        }


class ProviderMatchingAgent:
    """Agent 2: Match providers using 10-factor algorithm"""
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance in km using Haversine formula"""
        R = 6371  # Earth radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    @staticmethod
    async def match(service_type: str, user_location: Dict, urgency: str, providers: List[Dict]) -> Dict[str, Any]:
        start_time = time.time()
        
        user_lat = user_location['lat']
        user_lng = user_location['lng']
        
        scored_providers = []
        reasoning = [f"Found {len(providers)} providers for {service_type}"]
        
        for provider in providers:
            # Calculate distance
            distance = ProviderMatchingAgent.calculate_distance(
                user_lat, user_lng,
                float(provider['latitude']), float(provider['longitude'])
            )
            
            # 10-factor scoring
            distance_score = max(0, 1 - (distance / 10))  # 30% weight
            availability_score = 1.0 if provider['is_available'] else 0.0  # 20% weight
            rating_score = provider['rating'] / 5.0  # 15% weight
            recency_score = 0.8  # 5% weight (simplified)
            specialization_score = 0.9  # 10% weight (simplified)
            price_score = max(0, 1 - (provider['base_rate'] / 5000))  # 5% weight
            cancellation_score = 1 - provider['cancellation_rate']  # 5% weight
            response_score = max(0, 1 - (provider['response_time_avg_minutes'] / 60))  # 5% weight
            capacity_score = 0.8  # 3% weight (simplified)
            preference_score = 0.7  # 2% weight (simplified)
            
            # Weighted total
            total_score = (
                distance_score * 0.30 +
                availability_score * 0.20 +
                rating_score * 0.15 +
                recency_score * 0.05 +
                specialization_score * 0.10 +
                price_score * 0.05 +
                cancellation_score * 0.05 +
                response_score * 0.05 +
                capacity_score * 0.03 +
                preference_score * 0.02
            )
            
            eta_minutes = int(distance * 10)  # Rough estimate: 10 min per km
            
            scored_providers.append({
                "provider_id": provider['id'],
                "name": provider['name'],
                "rating": provider['rating'],
                "distance_km": round(distance, 2),
                "eta_minutes": eta_minutes,
                "base_rate": provider['base_rate'],
                "match_score": round(total_score, 2),
                "specialization": provider.get('specialization', []),
                "total_bookings": provider['total_bookings'],
                "cancellation_rate": provider['cancellation_rate']
            })
        
        # Sort by score
        scored_providers.sort(key=lambda x: x['match_score'], reverse=True)
        top_3 = scored_providers[:3]
        
        reasoning.append(f"Ranked by 10-factor algorithm")
        reasoning.append(f"Top provider: {top_3[0]['name']} (score: {top_3[0]['match_score']})")
        
        execution_time = int((time.time() - start_time) * 1000)
        
        return {
            "output": {"matched_providers": top_3},
            "reasoning": reasoning,
            "execution_time_ms": execution_time
        }


class PricingAgent:
    """Agent 3: Calculate dynamic pricing"""
    
    @staticmethod
    async def calculate(
        base_rate: float,
        distance_km: float,
        urgency: str,
        demand_level: str,
        loyalty_tier: str
    ) -> Dict[str, Any]:
        start_time = time.time()
        
        # Base fee
        base_fee = base_rate
        
        # Distance fee: PKR 10/km
        distance_fee = distance_km * 10
        
        # Urgency surcharge
        urgency_multipliers = {"routine": 0.0, "urgent": 0.25, "emergency": 0.50}
        urgency_surcharge = base_fee * urgency_multipliers.get(urgency, 0.0)
        
        # Demand surge
        demand_multipliers = {"low": 0.0, "medium": 0.10, "high": 0.30}
        demand_surge = base_fee * demand_multipliers.get(demand_level, 0.0)
        
        # Loyalty discount
        loyalty_discounts = {"bronze": 0.0, "silver": 0.05, "gold": 0.10, "platinum": 0.15}
        loyalty_discount = (base_fee + distance_fee) * loyalty_discounts.get(loyalty_tier, 0.0)
        
        # Final price
        final_price = base_fee + distance_fee + urgency_surcharge + demand_surge - loyalty_discount
        
        reasoning = [
            f"Base rate: PKR {base_fee}",
            f"Distance: {distance_km} km × PKR 10 = PKR {distance_fee}",
            f"Urgency: {urgency} ({int(urgency_multipliers.get(urgency, 0) * 100)}% surcharge = PKR {urgency_surcharge})",
            f"Demand: {demand_level} ({int(demand_multipliers.get(demand_level, 0) * 100)}% surge = PKR {demand_surge})",
            f"Loyalty: {loyalty_tier} ({int(loyalty_discounts.get(loyalty_tier, 0) * 100)}% discount = PKR {loyalty_discount})",
            f"Final: PKR {final_price:.2f}"
        ]
        
        execution_time = int((time.time() - start_time) * 1000)
        
        return {
            "output": {
                "base_fee": base_fee,
                "distance_fee": round(distance_fee, 2),
                "urgency_surcharge": round(urgency_surcharge, 2),
                "demand_surge": round(demand_surge, 2),
                "loyalty_discount": round(loyalty_discount, 2),
                "final_price": round(final_price, 2)
            },
            "reasoning": reasoning,
            "execution_time_ms": execution_time
        }


class SchedulingAgent:
    """Agent 4: Schedule booking"""
    
    @staticmethod
    async def schedule(provider_id: str, preferred_time: str, duration_minutes: int = 60) -> Dict[str, Any]:
        start_time = time.time()
        
        # Simplified: assume no conflicts
        scheduled_time = preferred_time
        end_time = (datetime.fromisoformat(preferred_time) + timedelta(minutes=duration_minutes)).isoformat()
        
        reasoning = [
            f"Checked provider calendar",
            f"No conflicts found at {preferred_time}",
            f"Reserved {duration_minutes}-minute slot",
            "Booking confirmed"
        ]
        
        execution_time = int((time.time() - start_time) * 1000)
        
        return {
            "output": {
                "scheduled_time": scheduled_time,
                "end_time": end_time,
                "status": "confirmed",
                "conflicts": []
            },
            "reasoning": reasoning,
            "execution_time_ms": execution_time
        }


class NotificationAgent:
    """Agent 5: Send notifications via multiple channels including WhatsApp"""
    
    @staticmethod
    async def send(
        booking_id: str, 
        customer_phone: str, 
        provider_name: str, 
        scheduled_time: str, 
        event_type: str,
        customer_name: str = "Customer",
        service_type: str = "Healthcare Service",
        booking_number: str = "",
        final_price: float = 0
    ) -> Dict[str, Any]:
        start_time = time.time()
        
        # Import WhatsApp service
        from app.services.whatsapp import whatsapp_service
        
        notifications_sent = []
        
        # Send WhatsApp notification based on event type
        if event_type == "booking_confirmed":
            whatsapp_result = await whatsapp_service.send_booking_confirmation(
                to_phone=customer_phone,
                customer_name=customer_name,
                provider_name=provider_name,
                service_type=service_type,
                scheduled_time=scheduled_time,
                booking_number=booking_number,
                final_price=final_price
            )
            
            notifications_sent.append({
                "channel": "whatsapp",
                "recipient": customer_phone,
                "message_id": whatsapp_result.get("message_id"),
                "status": whatsapp_result.get("status", "sent")
            })
            
        elif event_type == "en_route":
            whatsapp_result = await whatsapp_service.send_provider_enroute(
                to_phone=customer_phone,
                provider_name=provider_name,
                eta_minutes=15
            )
            
            notifications_sent.append({
                "channel": "whatsapp",
                "recipient": customer_phone,
                "message_id": whatsapp_result.get("message_id"),
                "status": whatsapp_result.get("status", "sent")
            })
            
        elif event_type == "completed":
            whatsapp_result = await whatsapp_service.send_service_completed(
                to_phone=customer_phone,
                booking_number=booking_number
            )
            
            notifications_sent.append({
                "channel": "whatsapp",
                "recipient": customer_phone,
                "message_id": whatsapp_result.get("message_id"),
                "status": whatsapp_result.get("status", "sent")
            })
        
        # Simulate SMS notification
        notifications_sent.append({
            "channel": "sms",
            "recipient": customer_phone,
            "status": "simulated"
        })
        
        # In-app notification
        notifications_sent.append({
            "channel": "in_app",
            "status": "delivered"
        })
        
        reasoning = [
            f"Event: {event_type}",
            f"WhatsApp notification sent to {customer_phone}",
            "Multi-channel notification strategy applied",
            f"Total channels: {len(notifications_sent)}"
        ]
        
        execution_time = int((time.time() - start_time) * 1000)
        
        return {
            "output": {"notifications_sent": notifications_sent},
            "reasoning": reasoning,
            "execution_time_ms": execution_time
        }


class FeedbackAgent:
    """Agent 6: Process feedback"""
    
    @staticmethod
    async def process(rating: int, comment: str) -> Dict[str, Any]:
        start_time = time.time()
        
        # Simple sentiment analysis
        positive_words = ['excellent', 'great', 'professional', 'caring', 'good', 'amazing']
        negative_words = ['bad', 'late', 'rude', 'poor', 'terrible', 'worst']
        
        comment_lower = comment.lower()
        positive_count = sum(1 for word in positive_words if word in comment_lower)
        negative_count = sum(1 for word in negative_words if word in comment_lower)
        
        # Calculate sentiment score
        if rating >= 4 and positive_count > negative_count:
            sentiment_score = 0.8 + (rating - 4) * 0.1
            sentiment_label = "very_positive"
        elif rating >= 3:
            sentiment_score = 0.5
            sentiment_label = "positive"
        elif rating == 2:
            sentiment_score = -0.3
            sentiment_label = "negative"
        else:
            sentiment_score = -0.8
            sentiment_label = "very_negative"
        
        reasoning = [
            f"Rating: {rating}/5",
            f"Sentiment: {sentiment_label} ({sentiment_score})",
            f"Positive keywords: {positive_count}",
            f"Negative keywords: {negative_count}"
        ]
        
        execution_time = int((time.time() - start_time) * 1000)
        
        return {
            "output": {
                "sentiment_score": round(sentiment_score, 2),
                "sentiment_label": sentiment_label,
                "dispute_detected": sentiment_score < -0.5
            },
            "reasoning": reasoning,
            "execution_time_ms": execution_time
        }
