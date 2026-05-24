from newspaper import Article
import requests
from bs4 import BeautifulSoup


def extract_text_from_url(url):
    """
    Extract clean article text from URL.
    Priority:
    1. newspaper3k (best for articles)
    2. BeautifulSoup fallback (for blocked sites)
    """

    print(f"🔍 Scraping URL: {url}")

    # =========================
    # 🔹 METHOD 1: newspaper3k
    # =========================
    try:
        article = Article(url)
        article.download()
        article.parse()

        text = article.text.strip()

        if text and len(text) > 200:
            print("✅ Extracted using newspaper3k")
            return text[:2000]

        else:
            print("⚠️ Newspaper3k returned insufficient text")

    except Exception as e:
        print("❌ Newspaper3k failed:", e)

    # =========================
    # 🔹 METHOD 2: BeautifulSoup (STRONGER)
    # =========================
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print("❌ Request failed with status:", response.status_code)
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted elements
        for tag in soup(["script", "style", "header", "footer", "nav", "aside", "noscript"]):
            tag.decompose()

        # 🔥 Try common article containers first
        article_tags = soup.find_all(["article", "section"])

        text = ""

        for tag in article_tags:
            paragraphs = tag.find_all("p")
            for p in paragraphs:
                content = p.get_text(strip=True)
                if len(content) > 50:
                    text += content + " "

        # 🔁 fallback to all <p> if above fails
        if len(text) < 200:
            paragraphs = soup.find_all("p")
            text = " ".join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 40])

        text = text.strip()

        if text and len(text) > 200:
            print("✅ Extracted using BeautifulSoup fallback")
            return text[:2000]

        print("⚠️ BeautifulSoup found insufficient text")
        return None

    except Exception as e:
        print("❌ BeautifulSoup fallback failed:", e)

    # =========================
    # 🔻 FINAL FAIL
    # =========================
    print("❌ All extraction methods failed")
    return None