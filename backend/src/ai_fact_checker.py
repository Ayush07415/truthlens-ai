from transformers import pipeline

# ====================================
# 🔥 LOAD AI FACT CHECK MODEL
# ====================================

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# ====================================
# 🔥 FACT VERIFICATION
# ====================================

def ai_fact_check(text):

    labels = [
        "true statement",
        "false statement",
        "misleading statement"
    ]

    result = classifier(
        text,
        labels
    )

    top_label = result["labels"][0]

    score = round(
        result["scores"][0] * 100,
        2
    )

    return {
        "label": top_label,
        "score": score
    }