
from core.security_analyzer import analyze_message


class PhishingAgent:

    def detect(self, message):
        result = analyze_message(message)

        return {
            "type": "Phishing Analysis",
            "risk_level": result["risk_level"],
            "risk_score": result["risk_score"],
            "reasons": result["reasons"]
        }
