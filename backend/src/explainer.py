# ====================================
# 🔥 AI EXPLANATION
# ====================================

def generate_explanation(
    prediction,
    clickbait_score,
    bias_score,
    suspicious_words,
    news_verified
):

    reasons = []

    if clickbait_score > 60:

        reasons.append(
            "High clickbait language detected"
        )

    if bias_score > 50:

        reasons.append(
            "Emotionally manipulative wording"
        )

    if len(suspicious_words) > 0:

        reasons.append(
            "Suspicious keywords found"
        )

    if not news_verified:

        reasons.append(
            "No trusted source verification"
        )

    if prediction == "FAKE":

        reasons.append(
            "AI model detected misinformation patterns"
        )

    return reasons