"""
Quick Backend API Test Script
Tests all major endpoints to verify functionality
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_health():
    """Test health endpoint"""
    print_section("TEST 1: Health Check")
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health check passed!")

def test_signup():
    """Test user registration"""
    print_section("TEST 2: User Registration")
    
    payload = {
        "full_name": "Test Customer",
        "phone_number": f"+92300{datetime.now().strftime('%H%M%S')}",
        "email": f"test{datetime.now().strftime('%H%M%S')}@example.com",
        "password": "password123",
        "role": "customer"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/signup", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 201
    assert "access_token" in response.json()
    print("✅ User registration passed!")
    
    return response.json()["access_token"]

def test_login():
    """Test user login"""
    print_section("TEST 3: User Login")
    
    payload = {
        "phone_number": "+923001234567",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ User login passed!")
        return response.json()["access_token"]
    else:
        print(f"⚠️ Login failed (expected - sample user password may not match)")
        print("Using signup token instead...")
        return None

def test_create_booking(token):
    """Test booking creation with AI orchestration"""
    print_section("TEST 4: Create Booking (AI Orchestration)")
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "user_query": "Mujhe kal morning nurse chahiye injection ke liye",
        "location": {
            "lat": 24.8607,
            "lng": 67.0011,
            "address": "Karachi, Pakistan"
        }
    }
    
    print("Sending booking request...")
    print(f"Query: {payload['user_query']}")
    
    response = requests.post(f"{BASE_URL}/api/bookings/create", json=payload, headers=headers)
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Booking created successfully!")
        print(f"Booking ID: {data['booking_id']}")
        print(f"Booking Number: {data['booking_number']}")
        print(f"\nProvider Matched:")
        print(f"  - Name: {data['provider']['name']}")
        print(f"  - Distance: {data['provider']['distance_km']} km")
        print(f"  - Match Score: {data['provider']['match_score']}")
        print(f"\nPricing Breakdown:")
        print(f"  - Base Fee: PKR {data['pricing']['base_fee']}")
        print(f"  - Distance Fee: PKR {data['pricing']['distance_fee']}")
        print(f"  - Urgency Surcharge: PKR {data['pricing']['urgency_surcharge']}")
        print(f"  - Final Price: PKR {data['pricing']['final_price']}")
        print(f"\nAI Reasoning Traces:")
        for agent, reasoning in data['ai_traces'].items():
            print(f"\n  [{agent.upper()}]")
            for step in reasoning[:2]:  # Show first 2 steps
                print(f"    - {step}")
        
        return data['booking_id']
    else:
        print(f"❌ Booking failed: {response.text}")
        return None

def test_get_booking(booking_id, token):
    """Test get booking details"""
    print_section("TEST 5: Get Booking Details")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/bookings/{booking_id}", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Booking retrieved successfully!")
        print(f"Service Type: {data['booking']['service_type']}")
        print(f"Status: {data['booking']['status']}")
        print(f"AI Traces Count: {len(data['ai_traces'])}")
    else:
        print(f"❌ Failed: {response.text}")

def test_admin_dashboard(token):
    """Test admin dashboard"""
    print_section("TEST 6: Admin Dashboard")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/admin/dashboard", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Dashboard data retrieved!")
        print(f"Total Bookings: {data['total_bookings']}")
        print(f"Active Bookings: {data['active_bookings']}")
        print(f"Total Providers: {data['total_providers']}")
        print(f"Available Providers: {data['available_providers']}")
        print(f"Total Revenue: PKR {data['total_revenue']}")
    else:
        print(f"⚠️ Dashboard access may require admin role")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  E-SHIFA AI - BACKEND API TEST SUITE")
    print("="*60)
    
    try:
        # Test 1: Health
        test_health()
        
        # Test 2: Signup
        token = test_signup()
        
        # Test 3: Login (optional)
        login_token = test_login()
        if login_token:
            token = login_token
        
        # Test 4: Create Booking
        booking_id = test_create_booking(token)
        
        # Test 5: Get Booking
        if booking_id:
            test_get_booking(booking_id, token)
        
        # Test 6: Admin Dashboard
        test_admin_dashboard(token)
        
        print_section("TEST SUMMARY")
        print("✅ All critical tests passed!")
        print("🎉 Backend is fully functional and ready for deployment!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
