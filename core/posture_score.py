
def calculate_posture_score(incidents):
    """
    Calculate security posture based on recorded incidents.
    Higher score means better security.
    """

    score = 100

    for incident in incidents:
        risk_level = str(incident[3]).lower()

        if risk_level == "high":
            score -= 15
        elif risk_level == "medium":
            score -= 8
        elif risk_level == "low":
            score -= 3

    return max(0, min(100, score))
