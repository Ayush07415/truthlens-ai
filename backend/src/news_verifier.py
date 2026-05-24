import requests

API_KEY = "e917fa2fb0a8428499df02ea1c71ba6b"

# ====================================
# 🔥 VERIFY NEWS ONLINE
# ====================================

def verify_online_news(query):

    try:

        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={query}"
            f"&language=en"
            f"&sortBy=publishedAt"
            f"&apiKey={API_KEY}"
        )

        response = requests.get(url)

        data = response.json()

        articles = data.get("articles", [])

        # No news found
        if len(articles) == 0:

            return {
                "verified": False,
                "message": "No trusted news found"
            }

        # Trusted news found
        return {
            "verified": True,
            "message": articles[0]["title"],
            "source": articles[0]["source"]["name"]
        }

    except Exception as e:

        print("NEWS API ERROR:", e)

        return {
            "verified": False,
            "message": "Verification unavailable"
        }