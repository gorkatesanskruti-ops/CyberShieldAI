
class RiskAgent:

    def calculate_risk(self, phishing_result, fraud_result):

        phishing_score = phishing_result["risk_score"]
        fraud_score = fraud_result["risk_score"]

        final_score = int(
            (phishing_score * 0.5) +
            (fraud_score * 0.5)
        )

        if final_score >= 60:
            risk_level = "High"
        elif final_score >= 30:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        reasons = (
            phishing_result.get("reasons", []) +
            fraud_result.get("reasons", [])
        )

        return {
            "risk_level": risk_level,
            "risk_score": final_score,
            "reasons": list(dict.fromkeys(reasons))
        }
