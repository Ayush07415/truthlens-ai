import pickle
import re
import textstat

from collections import Counter

from src.news_verifier import verify_online_news
from src.preprocessing import clean_text
from src.utils import get_fake_level
from src.fact_checker import check_fact_wikipedia
from src.explainer import generate_explanation

# ====================================
# 🔥 LOAD MODEL
# ====================================

model = pickle.load(
    open("models/model.pkl", "rb")
)

vectorizer = pickle.load(
    open("models/vectorizer.pkl", "rb")
)

# ====================================
# 🔥 SUSPICIOUS WORDS
# ====================================

FAKE_WORDS = [

    "shocking",
    "breaking",
    "secret",
    "viral",
    "fake",
    "fraud",
    "alert",
    "conspiracy",
    "banned",
    "exposed",
    "warning",
    "scam",
    "click here",
    "must watch",
    "unbelievable"
]

# ====================================
# 🔥 MAIN PREDICTION
# ====================================

def predict_news(
    text,
    extension_mode=False
):

    # ====================================
    # INPUT CHECK
    # ====================================

    if not text:

        return {

            "prediction": "INVALID",

            "confidence": 0,

            "credibility_score": 0,

            "level": "No input"
        }

    # ====================================
    # 🔥 FAST MODE FOR EXTENSION
    # ====================================

    if extension_mode:

        text = text[:800]

    # ====================================
    # CLEAN TEXT
    # ====================================

    cleaned_text = clean_text(text)

    word_count = len(
        cleaned_text.split()
    )

    # ====================================
    # VECTORIZE
    # ====================================

    vec = vectorizer.transform(
        [cleaned_text]
    )

    prob = model.predict_proba(vec)[0][1]

    # ====================================
    # DYNAMIC THRESHOLD
    # ====================================

    threshold = 0.80 if word_count < 25 else 0.75

    prediction = (

        "FAKE"

        if prob > threshold

        else "REAL"
    )

    # ====================================
    # CONFIDENCE
    # ====================================

    percent, level = get_fake_level(prob)

    credibility = round(
        (1 - prob) * 100,
        2
    )

    # ====================================
    # DEFAULT VALUES
    # ====================================

    news_check = {

        "verified": False,

        "message":
            "Skipped in fast mode"
    }

    fact_result = {

        "verified": False,

        "message":
            "Skipped in fast mode"
    }

    # ====================================
    # ONLINE NEWS CHECK
    # ====================================

    if not extension_mode:

        try:

            news_check = verify_online_news(
                text[:100]
            )

            if not news_check["verified"]:

                level = (
                    "No trusted sources found ⚠️"
                )

        except Exception:

            news_check = {

                "verified": False,

                "message":
                    "News verification unavailable"
            }

    # ====================================
    # FACT CHECK
    # ====================================

    try:

        fact_result = check_fact_wikipedia(
            text[:300]
        )

        if (
            fact_result and
            fact_result.get("verified")
        ):

            level = "Fact Verified ✅"

    except:

        pass

    # ====================================
    # 🔥 LIGHTWEIGHT AI LOGIC
    # ====================================

    if prediction == "FAKE":

        ai_explanation = (
            "This content contains suspicious patterns, "
            "emotional wording, or misleading signals "
            "commonly associated with fake news."
        )

    else:

        ai_explanation = (
            "This content appears relatively factual, "
            "balanced, and less emotionally manipulative."
        )

    # ====================================
    # LOW CONTEXT WARNING
    # ====================================

    if word_count < 25:

        level = "Low Context ⚠️"

    # ====================================
    # SUSPICIOUS WORDS
    # ====================================

    suspicious_words = []

    for word in FAKE_WORDS:

        if word in cleaned_text:

            suspicious_words.append(word)

    # ====================================
    # SENTENCE ANALYSIS
    # ====================================

    sentences = re.split(
        r'[.!?]+',
        cleaned_text
    )

    sentences = [

        s for s in sentences

        if s.strip()
    ]

    sentence_count = len(sentences)

    unique_words = len(

        set(
            cleaned_text.split()
        )
    )

    avg_sentence = 0

    if sentence_count > 0:

        avg_sentence = round(
            word_count / sentence_count,
            1
        )

    # ====================================
    # READABILITY INDEX
    # ====================================

    try:

        readability = round(

            textstat.flesch_reading_ease(
                cleaned_text
            ),

            1
        )

        readability = max(
            0,
            min(readability, 100)
        )

    except:

        readability = 50

    # ====================================
    # KEYWORDS
    # ====================================

    words = cleaned_text.split()

    common_words = Counter(
        words
    ).most_common(5)

    keywords = [

        w[0]

        for w in common_words
    ]

    # ====================================
    # CLAIM ANALYSIS
    # ====================================

    factual_accuracy = round(
        credibility
    )

    clickbait_score = round(
        prob * 100
    )

    # ====================================
    # SOURCE ANALYSIS
    # ====================================

    bias_score = round(
        prob * 70
    )

    emotion_score = round(
        prob * 80
    )

    # ====================================
    # SOURCE DETAILS
    # ====================================

    if news_check.get("verified"):

        source_name = (

            news_check.get(
                "source",
                "Verified Source"
            )
        )

        domain = "Trusted News"

        category = "Verified News"

    else:

        source_name = "User Submitted"

        domain = "Unknown Source"

        category = "Unverified"

    # ====================================
    # AI EXPLANATIONS
    # ====================================

    explanations = generate_explanation(

        prediction,

        clickbait_score,

        bias_score,

        suspicious_words,

        news_check.get("verified")
    )

    # ====================================
    # FINAL RESPONSE
    # ====================================

    return {

        "prediction":
            prediction,

        "confidence":
            percent,

        "credibility_score":
            credibility,

        "level":
            level,

        "news_verification":
            news_check,

        "fact_check":
            fact_result,

        "ai_explanation":
            ai_explanation,

        "explanations":
            explanations,

        "suspicious_words":
            suspicious_words,

        "factual_accuracy":
            factual_accuracy,

        "clickbait_score":
            clickbait_score,

        "bias_score":
            bias_score,

        "emotion_score":
            emotion_score,

        "source_name":
            source_name,

        "domain":
            domain,

        "category":
            category,

        "word_count":
            word_count,

        "sentence_count":
            sentence_count,

        "unique_words":
            unique_words,

        "avg_sentence":
            avg_sentence,

        "readability":
            readability,

        "keywords":
            keywords
    }