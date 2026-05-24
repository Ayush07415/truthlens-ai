def get_fake_level(prob):
    percent = round(prob * 100, 2)

    if percent > 75:
        level = "Highly Fake 🚨"
    elif percent > 50:
        level = "Moderately Fake ⚠️"
    else:
        level = "Likely Real ✅"

    return percent, level