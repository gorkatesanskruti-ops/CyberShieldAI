
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load Gmail settings
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "").strip()
EMAIL_PASSWORD = "".join(
    os.getenv("EMAIL_PASSWORD", "").split()
)
ALERT_EMAIL = os.getenv("ALERT_EMAIL", "").strip()


def send_security_alert(incident_type, description, risk_score):

    if not all([EMAIL_ADDRESS, EMAIL_PASSWORD, ALERT_EMAIL]):
        print("Email settings missing. Check your .env file.")
        return False

    message = EmailMessage()
    message["Subject"] = f"CyberShield AI Alert: {incident_type}"
    message["From"] = EMAIL_ADDRESS
    message["To"] = ALERT_EMAIL

    message.set_content(
        f"""
CYBERSHIELD AI SECURITY ALERT

A high-risk security incident was detected.

Incident: {incident_type}
Risk Score: {risk_score}/100
Description: {description}

Please investigate this incident.

CyberShield AI Security System
""",
        charset="utf-8"
    )

    try:
        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465,
            timeout=20
        ) as server:

            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(message)

        print("Security alert email sent successfully!")
        return True

    except Exception as error:
        print(f"Email sending failed: {error}")
        return False


# Test this file directly
if __name__ == "__main__":
    send_security_alert(
        "Connection Test",
        "Testing CyberShield AI Gmail integration.",
        85
    )
