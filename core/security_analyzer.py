
import re
from urllib.parse import urlparse


def analyze_message(message):
    score = 0
    reasons = []

    suspicious_keywords = [
        "urgent",
        "verify your account",
        "password",
        "account suspended",
        "send money",
        "bank account",
        "won a prize",
        "click here",
        "otp",
        "login immediately"
    ]

    text = message.lower()

    for keyword in suspicious_keywords:
        if keyword in text:
            score += 10
            reasons.append(f"Suspicious keyword: {keyword}")

    urls = re.findall(r'https?://\S+', message)

    if urls:
        score += 15
        reasons.append("Message contains a URL")

    score = min(score, 100)

    if score >= 60:
        risk = "High"
    elif score >= 30:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "risk_score": score,
        "risk_level": risk,
        "reasons": reasons
    }


def analyze_url(url):
    score = 0
    reasons = []

    parsed = urlparse(url)

    if parsed.scheme != "https":
        score += 20
        reasons.append("Website does not use HTTPS")

    if "@" in url:
        score += 25
        reasons.append("URL contains an @ symbol")

    if re.search(r'\d+\.\d+\.\d+\.\d+', parsed.netloc):
        score += 30
        reasons.append("URL uses an IP address")

    if len(url) > 75:
        score += 10
        reasons.append("Unusually long URL")

    if url.count("-") >= 3:
        score += 10
        reasons.append("URL contains many hyphens")

    score = min(score, 100)

    if score >= 60:
        risk = "High"
    elif score >= 30:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "risk_score": score,
        "risk_level": risk,
        "reasons": reasons
    }
