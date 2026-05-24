import requests

# ====================================
# 🔥 FACT CHECKER
# ====================================

def check_fact_wikipedia(text):

    try:

        # Small query
        query = " ".join(
            text.split()[:8]
        )

        # Wikipedia API
        url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + query.replace(" ", "_")
        )

        response = requests.get(
            url,
            timeout=5
        )

        # Failed request
        if response.status_code != 200:

            return {
                "verified": False,
                "message": "No fact verification found"
            }

        data = response.json()

        summary = data.get(
            "extract",
            ""
        )

        # Success
        if summary:

            return {
                "verified": True,
                "message": summary[:300]
            }

        # Empty summary
        return {
            "verified": False,
            "message": "No factual summary available"
        }

    except Exception as e:

        print("FACT CHECK ERROR:", e)

        return {
            "verified": False,
            "message": "Fact checker unavailable"
        }