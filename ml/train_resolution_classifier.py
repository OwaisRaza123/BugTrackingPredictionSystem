import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Algorithms
from sklearn.naive_bayes import MultinomialNB

# ==========================
# Load Dataset
# ==========================

data = pd.read_csv("dataset/resolution_labeled.csv")

print("Dataset Shape :", data.shape)

# Remove empty rows
data = data.dropna(subset=["Clean_Text"])

data["Clean_Text"] = data["Clean_Text"].astype(str)

# ==========================
# Features & Target
# ==========================

X = data["Clean_Text"]

y = data["Resolution_Label"]

# ==========================
# TF-IDF
# ==========================

tfidf = TfidfVectorizer(max_features=5000)

X = tfidf.fit_transform(X)

# ==========================
# Train Test Split
# ==========================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42

)

# ==========================
# Train Model
# ==========================

model = MultinomialNB()

print("Training Resolution Model...")

model.fit(X_train, y_train)

print("Training Completed")

# ==========================
# Prediction
# ==========================

prediction = model.predict(X_test)

accuracy = accuracy_score(

    y_test,

    prediction

)

print("\nAccuracy :", round(accuracy*100,2), "%")

print("\nClassification Report\n")

print(classification_report(y_test, prediction))

# ==========================
# Save Model
# ==========================

pickle.dump(

    model,

    open("ml/resolution_classifier.pkl", "wb")

)

pickle.dump(

    tfidf,

    open("ml/resolution_tfidf.pkl", "wb")

)

print("\nResolution Model Saved Successfully")