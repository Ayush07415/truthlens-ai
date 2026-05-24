# import pandas as pd
# import pickle
# import re
# from sklearn.model_selection import train_test_split
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
# from nltk.corpus import stopwords
# import nltk

# # 🔽 Download stopwords (runs once)
# nltk.download('stopwords')

# # 🔽 Load stopwords ONCE (very important for speed)
# stop_words = set(stopwords.words('english'))

# # 🔽 Fast clean function
# def clean_text(text):
#     text = str(text).lower()
#     text = re.sub(r'[^a-zA-Z]', ' ', text)
#     words = text.split()
#     words = [w for w in words if w not in stop_words]
#     return " ".join(words)

# # ===============================
# print("🔹 Loading dataset...")

# fake = pd.read_csv("../data/Fake.csv")
# real = pd.read_csv("../data/True.csv")

# print(f"Fake shape: {fake.shape}")
# print(f"Real shape: {real.shape}")

# # ===============================
# print("🔹 Adding labels...")

# fake["label"] = 1
# real["label"] = 0

# # ===============================
# print("🔹 Combining datasets...")

# df = pd.concat([fake, real], axis=0)

# # ===============================
# print("🔹 Shuffling dataset...")

# df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# # ===============================
# print("🔹 Preparing text...")

# if "title" in df.columns:
#     df["text"] = df["title"] + " " + df["text"]

# # ===============================
# print("🔹 Cleaning text (this may take time)...")

# df["text"] = df["text"].apply(clean_text)

# # ===============================
# print("🔹 Vectorizing text...")

# vectorizer = TfidfVectorizer(max_features=5000)
# X_vec = vectorizer.fit_transform(df["text"])

# # ===============================
# print("🔹 Splitting dataset...")

# X_train, X_test, y_train, y_test = train_test_split(
#     X_vec, df["label"], test_size=0.2, random_state=42
# )

# # ===============================
# print("🔹 Training model...")

# model = LogisticRegression(max_iter=1000)
# model.fit(X_train, y_train)

# # ===============================
# print("🔹 Evaluating model...")

# accuracy = model.score(X_test, y_test)
# print(f"✅ Accuracy: {accuracy:.4f}")

# # ===============================
# print("🔹 Saving model...")

# pickle.dump(model, open("models/model.pkl", "wb"))
# pickle.dump(vectorizer, open("models/vectorizer.pkl", "wb"))

# print("✅ Model and vectorizer saved successfully!")

# import pandas as pd
# import pickle
# import re
# from sklearn.model_selection import train_test_split
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
# from nltk.corpus import stopwords
# import nltk

# nltk.download('stopwords')

# # Load stopwords once (speed fix)
# stop_words = set(stopwords.words('english'))

# def clean_text(text):
#     text = str(text).lower()
#     text = re.sub(r'[^a-zA-Z]', ' ', text)
#     words = text.split()
#     words = [w for w in words if w not in stop_words]
#     return " ".join(words)

# print("🔹 Loading dataset...")
# fake = pd.read_csv("../data/Fake.csv")
# real = pd.read_csv("../data/True.csv")

# # 🔥 BALANCE DATASET
# min_len = min(len(fake), len(real))
# fake = fake.sample(min_len, random_state=42)
# real = real.sample(min_len, random_state=42)

# fake["label"] = 1
# real["label"] = 0

# df = pd.concat([fake, real])

# # Shuffle
# df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# # Combine title + text
# if "title" in df.columns:
#     df["text"] = df["title"] + " " + df["text"]

# print("🔹 Cleaning text...")
# df["text"] = df["text"].apply(clean_text)

# X = df["text"]
# y = df["label"]

# print("🔹 Vectorizing...")
# vectorizer = TfidfVectorizer(max_features=5000)
# X_vec = vectorizer.fit_transform(X)

# X_train, X_test, y_train, y_test = train_test_split(
#     X_vec, y, test_size=0.2, random_state=42
# )

# print("🔹 Training model...")
# model = LogisticRegression(max_iter=1000)
# model.fit(X_train, y_train)

# accuracy = model.score(X_test, y_test)
# print(f"✅ Accuracy: {accuracy:.4f}")

# pickle.dump(model, open("models/model.pkl", "wb"))
# pickle.dump(vectorizer, open("models/vectorizer.pkl", "wb"))

# print("✅ Model saved!")
import pandas as pd
import pickle
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)

# =========================
print("🔹 Loading dataset...")

fake = pd.read_csv("../data/Fake.csv")
real = pd.read_csv("../data/True.csv")

# =========================
print("🔹 Balancing dataset...")

min_len = min(len(fake), len(real))
fake = fake.sample(min_len, random_state=42)
real = real.sample(min_len, random_state=42)

# =========================
print("🔹 Adding labels...")

fake["label"] = 1
real["label"] = 0

# =========================
print("🔹 Combining...")

df = pd.concat([fake, real], axis=0)

# Shuffle
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# =========================
print("🔹 Preparing text...")

# 🔥 USE ONLY TITLE + TEXT
df["content"] = df["title"] + " " + df["text"]

# =========================
print("🔹 Cleaning text...")

df["content"] = df["content"].apply(clean_text)

X = df["content"]
y = df["label"]

# =========================
print("🔹 Vectorizing...")

vectorizer = TfidfVectorizer(
    max_features=7000,
    ngram_range=(1, 2)
)
X_vec = vectorizer.fit_transform(X)

# =========================
print("🔹 Splitting...")

X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42
)

# =========================
print("🔹 Training...")

#model = LogisticRegression(max_iter=1000)
model = MultinomialNB()
model.fit(X_train, y_train)

# =========================
print("🔹 Evaluating...")

accuracy = model.score(X_test, y_test)
print(f"✅ Accuracy: {accuracy:.4f}")

# =========================
print("🔹 Saving...")

pickle.dump(model, open("models/model.pkl", "wb"))
pickle.dump(vectorizer, open("models/vectorizer.pkl", "wb"))

print("✅ Model saved successfully!")