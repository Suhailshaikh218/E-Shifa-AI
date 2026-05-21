"""
WhatsApp Webhooks API
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import Response
import os

router = APIRouter(tags=["Webhooks"])

WEBHOOK_VERIFY_TOKEN = os.getenv("WHATSAPP_WEBHOOK_VERIFY_TOKEN", "eshifa_webhook_secure_2024")


@router.get("/api/webhooks/whatsapp")
async def verify_webhook(request: Request):
    """
    Meta calls this to verify your Callback URL.
    Returns the hub.challenge as plain text.
    """
    params = dict(request.query_params)
    mode      = params.get("hub.mode")
    token     = params.get("hub.verify_token")
    challenge = params.get("hub.challenge", "")

    print(f"[WEBHOOK VERIFY] mode={mode}  token={token}  challenge={challenge}")

    if mode == "subscribe" and token == WEBHOOK_VERIFY_TOKEN:
        print("✅ Webhook verified!")
        return Response(content=challenge, media_type="text/plain")

    raise HTTPException(status_code=403, detail="Verification token mismatch")


@router.post("/api/webhooks/whatsapp")
async def receive_webhook(request: Request):
    """Receive incoming WhatsApp messages and status updates."""
    try:
        body = await request.json()
        print("\n📱 WHATSAPP WEBHOOK RECEIVED")

        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})

                for message in value.get("messages", []):
                    from_number  = message.get("from")
                    message_type = message.get("type")
                    print(f"  📨 From: +{from_number}  type={message_type}")
                    if message_type == "text":
                        print(f"  Content: {message.get('text', {}).get('body', '')}")

                for status in value.get("statuses", []):
                    print(f"  📊 Status: {status.get('status')} → +{status.get('recipient_id')}")

        return {"status": "ok"}
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return {"status": "error"}


@router.get("/api/webhooks/whatsapp/info")
async def webhook_info():
    """Returns the Callback URL and Verify Token to paste into Meta dashboard."""
    return {
        "callback_url_path": "/api/webhooks/whatsapp",
        "verify_token": WEBHOOK_VERIFY_TOKEN,
        "instructions": {
            "step1": "Copy the verify_token value above",
            "step2": "In Meta dashboard → WhatsApp → Configuration → Webhooks",
            "step3": "Callback URL = https://YOUR_BACKEND_URL/api/webhooks/whatsapp",
            "step4": "Verify Token = paste the verify_token value",
            "step5": "Click 'Verify and Save'",
            "step6": "Subscribe to 'messages' and 'message_status' fields"
        }
    }
