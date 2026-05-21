"""
Test WhatsApp Integration
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.whatsapp import whatsapp_service


async def test_whatsapp():
    """Test WhatsApp service"""
    
    print("\n" + "="*60)
    print("  WHATSAPP INTEGRATION TEST")
    print("="*60 + "\n")
    
    # Test 1: Booking Confirmation
    print("📱 Test 1: Booking Confirmation Message")
    print("-" * 60)
    
    result = await whatsapp_service.send_booking_confirmation(
        to_phone="+923001234567",
        customer_name="Ahmed Khan",
        provider_name="Nurse Fatima",
        service_type="Home Nurse",
        scheduled_time="2024-05-22 10:00 AM",
        booking_number="ESH12345678",
        final_price=1500
    )
    
    print(f"Status: {result.get('status')}")
    print(f"Success: {result.get('success')}")
    if result.get('message_id'):
        print(f"Message ID: {result.get('message_id')}")
    if result.get('error'):
        print(f"Error: {result.get('error')}")
    
    print("\n" + "="*60)
    
    # Test 2: Provider En Route
    print("📱 Test 2: Provider En Route Message")
    print("-" * 60)
    
    result = await whatsapp_service.send_provider_enroute(
        to_phone="+923001234567",
        provider_name="Nurse Fatima",
        eta_minutes=15
    )
    
    print(f"Status: {result.get('status')}")
    print(f"Success: {result.get('success')}")
    
    print("\n" + "="*60)
    
    # Test 3: Service Completed
    print("📱 Test 3: Service Completed Message")
    print("-" * 60)
    
    result = await whatsapp_service.send_service_completed(
        to_phone="+923001234567",
        booking_number="ESH12345678"
    )
    
    print(f"Status: {result.get('status')}")
    print(f"Success: {result.get('success')}")
    
    print("\n" + "="*60)
    print("\n✅ WhatsApp Integration Test Complete!\n")
    
    # Check configuration
    print("📋 Configuration Status:")
    print("-" * 60)
    
    if whatsapp_service.phone_number_id:
        print(f"✅ Phone Number ID: {whatsapp_service.phone_number_id[:10]}...")
    else:
        print("⚠️  Phone Number ID: Not configured (simulation mode)")
    
    if whatsapp_service.access_token:
        print(f"✅ Access Token: {whatsapp_service.access_token[:20]}...")
    else:
        print("⚠️  Access Token: Not configured (simulation mode)")
    
    if whatsapp_service.business_account_id:
        print(f"✅ Business Account ID: {whatsapp_service.business_account_id}")
    else:
        print("⚠️  Business Account ID: Not configured (simulation mode)")
    
    print("\n" + "="*60)
    print("\n💡 To enable real WhatsApp messages:")
    print("   1. Get credentials from: https://developers.facebook.com/apps/")
    print("   2. Add to backend/.env:")
    print("      WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id")
    print("      WHATSAPP_ACCESS_TOKEN=your_access_token")
    print("      WHATSAPP_BUSINESS_ACCOUNT_ID=your_business_account_id")
    print("\n   See WHATSAPP_SETUP_GUIDE.md for detailed instructions\n")


if __name__ == "__main__":
    asyncio.run(test_whatsapp())
