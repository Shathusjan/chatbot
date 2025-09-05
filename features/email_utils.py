import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = "sivaneswaranshathusjan@gmail.com"  # your company address
MAILTRAP_USER = os.getenv("MAILTRAP_USER")
MAILTRAP_PASS = os.getenv("MAILTRAP_PW")
SMTP_SERVER = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 587

def send_quotation_email(user_email, quotation_text):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = user_email
        msg["Subject"] = "Your Quotation from Magnolia Cakes"

        body = f"""
Hello,

Here’s your quotation:

{quotation_text}

Thank you for choosing Magnolia Cakes 🎂
"""
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(MAILTRAP_USER, MAILTRAP_PASS)
            server.sendmail(SENDER_EMAIL, [user_email, SENDER_EMAIL], msg.as_string())

        print("✅ Quotation sent")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False