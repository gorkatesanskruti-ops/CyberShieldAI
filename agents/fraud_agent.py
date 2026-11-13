
class FraudAgent:

    def detect(self, message):
        text = message.lower()

        score = 0
        reasons = []

        fraud_keywords = [
            "send money",
            "bank details",
            "upi",
            "otp",
            "refund",
            "lottery",
            "prize money",
            "investment guaranteed",
            "account blocked",
            "payment failed",
            "claim reward",
            "transfer now"
        ]

        for keyword in fraud_keywords:
            if keyword in text:
                score += 15
                reasons.append(f"Fraud indicator: {keyword}")

        score = min(score, 100)

        if score >= 60:
            risk = "High"
        elif score >= 30:
            risk = "Medium"
        else:
            risk = "Low"

        return {
            "type": "Fraud Analysis",
            "risk_level": risk,
            "risk_score": score,
            "reasons": reasons
        }
