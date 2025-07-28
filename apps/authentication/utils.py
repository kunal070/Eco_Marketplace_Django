from django.contrib.auth.tokens import PasswordResetTokenGenerator
from dotenv import load_dotenv
from twilio.rest import Client
from django.conf import settings
import os

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    pass

email_verification_token = EmailVerificationTokenGenerator()

load_dotenv()

def send_verification_code(phone_number, code):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_phone = os.getenv("TWILIO_PHONE_NUMBER")
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f'Your verification code is {code}',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid