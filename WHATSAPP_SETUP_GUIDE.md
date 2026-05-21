# 📱 WhatsApp Business API Integration Guide

## ✅ What's Already Done

I've integrated WhatsApp Business API into your E-Shifa AI backend:

✅ **WhatsApp Service Created** (`backend/app/services/whatsapp.py`)
- Send template messages
- Send text messages
- Booking confirmation messages
- Provider en-route notifications
- Service completion notifications

✅ **Notification Agent Updated** (`backend/app/services/ai_agents.py`)
- Integrated with WhatsApp service
- Multi-channel notifications (WhatsApp + SMS + In-app)
- Event-based messaging

✅ **Booking API Updated** (`backend/app/api/bookings.py`)
- Passes customer details to WhatsApp
- Sends booking confirmation via WhatsApp
- Includes booking number and price

---

## 🔧 Setup Steps (Meta WhatsApp Business API)

### Step 1: Create Meta App

1. Go to: https://developers.facebook.com/apps/
2. Click **"Create App"**
3. Select **"Business"** as app type
4. Fill in details:
   - App Name: `E-Shifa AI`
   - Contact Email: Your email
5. Click **"Create App"**

### Step 2: Add WhatsApp Product

1. In your app dashboard, find **"WhatsApp"**
2. Click **"Set Up"**
3. You'll see the WhatsApp setup page

### Step 3: Get Your Credentials

#### A. Phone Number ID
1. Go to **WhatsApp > API Setup**
2. You'll see **"Phone number ID"** (looks like: `123456789012345`)
3. Copy this number

#### B. Access Token
1. On the same page, you'll see **"Temporary access token"**
2. Copy this token (starts with `EAA...`)
3. **Note**: This is temporary. For production, generate a permanent token:
   - Go to **WhatsApp > Configuration**
   - Click **"Generate Token"**
   - Select permissions: `whatsapp_business_messaging`
   - Copy the permanent token

#### C. Business Account ID
1. Go to **WhatsApp > Getting Started**
2. You'll see **"WhatsApp Business Account ID"**
3. Copy this ID

### Step 4: Add Credentials to .env

Open `backend/.env` and add:

```env
WHATSAPP_PHONE_NUMBER_ID=123456789012345
WHATSAPP_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxxxxx
WHATSAPP_BUSINESS_ACCOUNT_ID=987654321098765
```

### Step 5: Configure Webhooks (For Receiving Messages)

1. Go to **WhatsApp > Configuration**
2. Click **"Edit"** next to Webhook
3. Enter:
   - **Callback URL**: `https://your-backend-url.run.app/api/webhooks/whatsapp`
   - **Verify Token**: Create a random string (e.g., `eshifa_webhook_2024`)
4. Subscribe to fields:
   - `messages`
   - `message_status`
5. Click **"Verify and Save"**

### Step 6: Add Test Phone Number

1. Go to **WhatsApp > API Setup**
2. Under **"To"**, click **"Manage phone number list"**
3. Add your phone number (with country code, e.g., `+923001234567`)
4. You'll receive a verification code on WhatsApp
5. Enter the code to verify

### Step 7: Test the Integration

Run this test:

```bash
cd backend
python -c "
import asyncio
from app.services.whatsapp import whatsapp_service

async def test():
    result = await whatsapp_service.send_booking_confirmation(
        to_phone='+923001234567',  # Your verified number
        customer_name='Ahmed Khan',
        provider_name='Nurse Fatima',
        service_type='Home Nurse',
        scheduled_time='2024-05-22 10:00 AM',
        booking_number='ESH12345678',
        final_price=1500
    )
    print(result)

asyncio.run(test())
"
```

---

## 📋 WhatsApp Message Templates

For production, you need to create **approved message templates** in Meta dashboard.

### Template 1: Booking Confirmation

**Name**: `booking_confirmation`
**Category**: `TRANSACTIONAL`
**Language**: English

**Template Content**:
```
🏥 *E-Shifa AI - Booking Confirmed*

Hello {{1}}!

✅ Your {{2}} booking has been confirmed.

📋 *Details:*
• Provider: {{3}}
• Time: {{4}}
• Booking #: {{5}}
• Amount: {{6}}

Your healthcare provider will arrive at the scheduled time.

Thank you! 🙏
```

**Parameters**:
1. Customer name
2. Service type
3. Provider name
4. Scheduled time
5. Booking number
6. Price

### Template 2: Provider En Route

**Name**: `provider_enroute`
**Category**: `TRANSACTIONAL`

**Template Content**:
```
🚗 *Provider En Route*

{{1}} is on the way!

⏱️ Estimated arrival: {{2}} minutes

Please be ready. Thank you! 🙏
```

**Parameters**:
1. Provider name
2. ETA minutes

### Template 3: Service Completed

**Name**: `service_completed`
**Category**: `TRANSACTIONAL`

**Template Content**:
```
✅ *Service Completed*

Your service (Booking #{{1}}) has been completed.

⭐ Please rate your experience!

Thank you for using E-Shifa AI! 🏥
```

**Parameters**:
1. Booking number

---

## 🧪 Testing Without Production Setup

If you don't have WhatsApp credentials yet, the system will **simulate** sending messages:

```python
# In whatsapp.py, if credentials are empty:
if not self.phone_number_id or not self.access_token:
    print("⚠️ WhatsApp not configured - simulating send")
    return {
        "success": True,
        "message_id": "simulated_msg_id",
        "status": "simulated"
    }
```

This allows you to:
- ✅ Test the complete booking flow
- ✅ See WhatsApp notifications in logs
- ✅ Demo the system without real WhatsApp setup
- ✅ Deploy and test other features

---

## 📊 How It Works

### Booking Flow with WhatsApp

1. **User creates booking** via API
2. **AI agents process** the request
3. **Booking confirmed** in database
4. **NotificationAgent triggered**:
   ```python
   notification_result = await NotificationAgent.send(
       booking_id=booking_id,
       customer_phone="+923001234567",
       provider_name="Nurse Fatima",
       scheduled_time="2024-05-22 10:00 AM",
       event_type="booking_confirmed",
       customer_name="Ahmed Khan",
       service_type="Home Nurse",
       booking_number="ESH12345678",
       final_price=1500
   )
   ```
5. **WhatsApp message sent** to customer
6. **Response logged** in AI traces

### Message Types

| Event | WhatsApp Message | When Sent |
|-------|-----------------|-----------|
| `booking_confirmed` | Booking confirmation with details | After booking created |
| `en_route` | Provider is on the way | When provider starts journey |
| `completed` | Service completed, rate us | After service completion |

---

## 🔐 Security Best Practices

### 1. Protect Access Token
```env
# Never commit this to Git!
WHATSAPP_ACCESS_TOKEN=EAAxxxxxxxxx
```

### 2. Use Environment Variables
```python
# Always load from environment
self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
```

### 3. Validate Phone Numbers
```python
# Remove + sign for API
to_phone.replace("+", "")
```

### 4. Handle Errors Gracefully
```python
try:
    response = await client.post(url, json=payload, headers=headers)
except Exception as e:
    print(f"❌ WhatsApp Error: {str(e)}")
    return {"success": False, "error": str(e)}
```

---

## 💰 Pricing

### Meta WhatsApp Business API

**Free Tier**:
- 1,000 free conversations per month
- Conversation = 24-hour window with a user

**Paid Tier** (after free tier):
- Service conversations: $0.005 - $0.02 per conversation
- Marketing conversations: $0.01 - $0.04 per conversation

**For Hackathon**: Free tier is more than enough!

---

## 🐛 Troubleshooting

### Error: "Phone number not verified"
**Solution**: Add your phone number in Meta dashboard under "To" section

### Error: "Invalid access token"
**Solution**: Generate a new token from Meta dashboard

### Error: "Template not found"
**Solution**: Create and approve templates in Meta dashboard first

### Error: "Webhook verification failed"
**Solution**: Check callback URL and verify token match

### Messages not sending?
**Check**:
1. ✅ Credentials in `.env` are correct
2. ✅ Phone number is verified in Meta dashboard
3. ✅ Access token is not expired
4. ✅ Backend is running

---

## 📱 Demo Without Real WhatsApp

For hackathon demo, you can show:

1. **Simulated Messages**: System logs show what would be sent
2. **API Response**: Shows WhatsApp notification status
3. **AI Traces**: Display WhatsApp notification in reasoning logs
4. **Screenshots**: Show Meta dashboard setup

---

## 🚀 Production Deployment

### Before Going Live:

1. ✅ Get permanent access token (not temporary)
2. ✅ Create and approve all message templates
3. ✅ Add all customer phone numbers OR
4. ✅ Complete Business Verification (for unlimited numbers)
5. ✅ Set up webhooks for two-way communication
6. ✅ Configure rate limiting
7. ✅ Add error monitoring

### Business Verification (Optional):

To send messages to any phone number (not just verified ones):
1. Complete Meta Business Verification
2. Provide business documents
3. Wait for approval (1-2 weeks)

For hackathon, you can use test numbers only!

---

## 📞 Support

### Meta WhatsApp Support:
- Docs: https://developers.facebook.com/docs/whatsapp
- Community: https://developers.facebook.com/community/

### E-Shifa AI Support:
- Check logs: Backend terminal shows WhatsApp status
- Test endpoint: `POST /api/bookings/create`
- View traces: `GET /api/admin/ai-traces`

---

## ✅ Checklist

- [ ] Created Meta app
- [ ] Added WhatsApp product
- [ ] Got Phone Number ID
- [ ] Got Access Token
- [ ] Got Business Account ID
- [ ] Added credentials to `.env`
- [ ] Added test phone number
- [ ] Verified phone number
- [ ] Created message templates (optional for demo)
- [ ] Tested sending message
- [ ] Configured webhooks (optional)

---

**Status**: WhatsApp integration is **READY**! 

- ✅ Code implemented
- ✅ Service created
- ✅ Agents updated
- ⚠️ Needs Meta credentials (or works in simulation mode)

**For Demo**: You can show the system working in simulation mode, then add real credentials later for production!
