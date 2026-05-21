"""
WhatsApp Business API Integration
Send notifications via Meta WhatsApp Business Platform
"""
import httpx
import os
from typing import Dict, Any, Optional
from app.core.config import settings


class WhatsAppService:
    """WhatsApp Business API Service"""
    
    def __init__(self):
        self.api_url = "https://graph.facebook.com/v18.0"
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
        self.business_account_id = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID", "")
    
    async def send_template_message(
        self,
        to_phone: str,
        template_name: str,
        language_code: str = "en",
        parameters: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Send WhatsApp template message
        
        Args:
            to_phone: Recipient phone number (with country code, e.g., +923001234567)
            template_name: Approved template name
            language_code: Language code (en, ur, etc.)
            parameters: Template parameters
        """
        
        if not self.phone_number_id or not self.access_token:
            print("⚠️ WhatsApp credentials not configured - simulating send")
            return {
                "success": True,
                "message_id": "simulated_msg_id",
                "status": "simulated"
            }
        
        url = f"{self.api_url}/{self.phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # Build template components
        components = []
        if parameters:
            components.append({
                "type": "body",
                "parameters": [{"type": "text", "text": param} for param in parameters]
            })
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone.replace("+", ""),  # Remove + sign
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                },
                "components": components
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "message_id": data.get("messages", [{}])[0].get("id"),
                        "status": "sent"
                    }
                else:
                    print(f"❌ WhatsApp API Error: {response.status_code} - {response.text}")
                    return {
                        "success": False,
                        "error": response.text,
                        "status": "failed"
                    }
        except Exception as e:
            print(f"❌ WhatsApp Send Error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "status": "failed"
            }
    
    async def send_text_message(
        self,
        to_phone: str,
        message: str
    ) -> Dict[str, Any]:
        """
        Send simple text message (only works within 24-hour window)
        
        Args:
            to_phone: Recipient phone number
            message: Text message to send
        """
        
        if not self.phone_number_id or not self.access_token:
            print(f"⚠️ WhatsApp not configured - would send: {message}")
            return {
                "success": True,
                "message_id": "simulated_msg_id",
                "status": "simulated"
            }
        
        url = f"{self.api_url}/{self.phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone.replace("+", ""),
            "type": "text",
            "text": {
                "body": message
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "message_id": data.get("messages", [{}])[0].get("id"),
                        "status": "sent"
                    }
                else:
                    print(f"❌ WhatsApp API Error: {response.status_code} - {response.text}")
                    return {
                        "success": False,
                        "error": response.text,
                        "status": "failed"
                    }
        except Exception as e:
            print(f"❌ WhatsApp Send Error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "status": "failed"
            }
    
    async def send_booking_confirmation(
        self,
        to_phone: str,
        customer_name: str,
        provider_name: str,
        service_type: str,
        scheduled_time: str,
        booking_number: str,
        final_price: float
    ) -> Dict[str, Any]:
        """
        Send booking confirmation via WhatsApp template
        
        Template parameters:
        1. Customer name
        2. Service type
        3. Provider name
        4. Scheduled time
        5. Booking number
        6. Price
        """
        
        # Use template if configured, otherwise send text
        if self.phone_number_id and self.access_token:
            # Try template first (requires pre-approved template)
            return await self.send_template_message(
                to_phone=to_phone,
                template_name="booking_confirmation",  # Must be created in Meta dashboard
                language_code="en",
                parameters=[
                    customer_name,
                    service_type,
                    provider_name,
                    scheduled_time,
                    booking_number,
                    f"PKR {final_price}"
                ]
            )
        else:
            # Fallback to text message (simulation)
            message = f"""🏥 *E-Shifa AI - Booking Confirmed*

Hello {customer_name}!

✅ Your booking has been confirmed.

📋 *Booking Details:*
• Service: {service_type}
• Provider: {provider_name}
• Time: {scheduled_time}
• Booking #: {booking_number}
• Amount: PKR {final_price}

Your healthcare provider will arrive at the scheduled time.

Thank you for choosing E-Shifa AI! 🙏"""
            
            return await self.send_text_message(to_phone, message)
    
    async def send_provider_enroute(
        self,
        to_phone: str,
        provider_name: str,
        eta_minutes: int
    ) -> Dict[str, Any]:
        """Send provider en-route notification"""
        
        message = f"""🚗 *Provider En Route*

{provider_name} is on the way!

⏱️ Estimated arrival: {eta_minutes} minutes

Please be ready. Thank you! 🙏"""
        
        return await self.send_text_message(to_phone, message)
    
    async def send_service_completed(
        self,
        to_phone: str,
        booking_number: str
    ) -> Dict[str, Any]:
        """Send service completion notification"""
        
        message = f"""✅ *Service Completed*

Your service (Booking #{booking_number}) has been completed.

⭐ Please rate your experience to help us improve!

Thank you for using E-Shifa AI! 🏥"""
        
        return await self.send_text_message(to_phone, message)


# Global instance
whatsapp_service = WhatsAppService()
