# 🧠 TruthLens AI — Fake News Detection System

TruthLens AI is an advanced AI-powered Fake News Detection platform that analyzes news articles, URLs, and social media content to determine credibility, detect manipulation patterns, and provide intelligent explanations.

---

# 🚀 Features

✅ AI Fake News Detection  
✅ AI Explanation System  
✅ Fact Verification  
✅ URL Analysis  
✅ Linguistic Analysis  
✅ Source Analysis  
✅ Chrome Extension  
✅ Modern Futuristic UI  

---

# 🛠️ Tech Stack

## Frontend
- HTML5
- CSS3
- JavaScript

## Backend
- Python
- Flask
- Flask-CORS

## Machine Learning
- Scikit-learn
- TF-IDF Vectorizer
- NLP preprocessing

## NLP & Utilities
- NLTK
- BeautifulSoup4
- Requests
- Textstat

## Browser Extension
- Chrome Extension Manifest V3

---

# 📂 Project Structure

```bash
fake_news_detector/
│
├── backend/
│   ├── app.py
│   ├── train.py
│   ├── requirements.txt
│   │
│   ├── models/
│   │   ├── model.pkl
│   │   └── vectorizer.pkl
│   │
│   └── src/
│       ├── predict.py
│       ├── preprocessing.py
│       ├── scraper.py
│       ├── fact_checker.py
│       ├── news_verifier.py
│       ├── explainer.py
│       └── utils.py
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
├── chrome-extension/
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   ├── content.js
│   ├── background.js
│   └── style.css
│
├── data/
│   ├── Fake.csv
│   └── True.csv
│
└── README.md
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Ayush07415/truthlens-ai.git
cd truthlens-ai
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate Environment:

```bash
.venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

# 🧠 Train ML Model

```bash
python backend/train.py
```

This generates:

- model.pkl
- vectorizer.pkl

---

# 🚀 Run Backend Server

```bash
cd backend
python app.py
```

Backend runs on:

```bash
http://127.0.0.1:5000
```

---

# 🌐 Run Frontend

Open:

```bash
frontend/index.html
```

using VS Code Live Server.

Frontend runs on:

```bash
http://127.0.0.1:5500
```

---

# 🧩 Chrome Extension Setup

## 1️⃣ Open Chrome Extensions

```bash
chrome://extensions
```

Enable:

- Developer Mode

---

## 2️⃣ Load Extension

Click:

```bash
Load unpacked
```

Select:

```bash
chrome-extension/
```

---

# 📊 Main Features

## 🔍 AI Verdict Dashboard

- REAL / FAKE Detection
- Confidence Meter
- Credibility Score

## 🧠 AI Explanations

- Emotional manipulation detection
- Clickbait analysis
- Suspicious wording detection

## 📖 Linguistic Analysis

- Readability Index
- Sentence analysis
- Word complexity

## 🌍 Source Analysis

- Bias score
- Emotion score
- Source credibility

## 🔎 Fact Verification

- Wikipedia-based fact checking
- Online verification system

## 🧩 Chrome Extension

- Instagram analysis
- News article scanning
- Floating AI analysis UI

---

# 🚀 Future Improvements

- Real-time News API
- Multi-language detection
- Advanced AI explanations
- Cloud deployment
- Mobile app
- Export reports

---

# 👨‍💻 Author

## Ayush Sarkar

GitHub:
https://github.com/Ayush07415

---

# ⭐ Support

If you like this project:

⭐ Star the repository  
🍴 Fork the repository  
🚀 Contribute improvements
