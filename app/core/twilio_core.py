from fastapi import HTTPException
from pydantic import BaseModel, Field, constr
from app.core.config import Settings
from twilio.rest import Client
from random import randint

from app.schemas.users import OTPRequest, OTPVerification


settings = Settings()


TWILIO_ACCOUNT_SID = Settings.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = Settings.TWILIO_AUTH_TOKEN
TWILIO_MESSAGING_SERVICE_SID = Settings.TWILIO_SERVICES_ID


client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

otp_storage = {}


def send_otp(phone_number: str, otp: int):
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        messaging_service_sid=TWILIO_MESSAGING_SERVICE_SID,  # Use Messaging Service SID
        to=phone_number,
    )
    return message.sid


async def send_otp_endpoint(request: OTPRequest):
    otp = randint(100000, 999999)  # Generate a 6-digit OTP
    otp_storage[request.phone_number] = otp

    try:
        send_otp(request.phone_number, otp)
        return {"message": "OTP sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def verify_otp(request: OTPVerification):
    stored_otp = otp_storage.get(request.phone_number)

    if stored_otp is None:
        raise HTTPException(status_code=400, detail="OTP not found or expired")

    if stored_otp != request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    otp_storage.pop(request.phone_number)  # Remove OTP after successful verification
    return {"message": "OTP verified successfully"}
