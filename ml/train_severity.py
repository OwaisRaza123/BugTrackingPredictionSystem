import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.naive_bayes import MultinomialNB


# ==========================
# Load Dataset
# ==========================

data = pd.read_csv("dataset/severity_processed.csv")

# Remove rows where Clean_Text is empty
data = data.dropna(subset=["Clean_Text"])

# Convert to string
data["Clean_Text"] = data["Clean_Text"].astype(str)

print("Dataset Shape :", data.shape)



# ==========================
# Features & Labels
# ==========================

X = data["Clean_Text"]

y = data["Severity"]


# ==========================
# TF-IDF
# ==========================

tfidf = TfidfVectorizer(
    max_features=5000
)

X = tfidf.fit_transform(X)

print("TF-IDF Shape :", X.shape)


# ==========================
# Train/Test Split
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

model.fit(

    X_train,

    y_train

)


# ==========================
# Prediction
# ==========================

prediction = model.predict(

    X_test

)


accuracy = accuracy_score(

    y_test,

    prediction

)


print()

print("Accuracy :", round(accuracy*100,2), "%")


# ==========================
# Save Model
# ==========================

joblib.dump(

    model,

    "ml/severity_model.pkl"

)

joblib.dump(

    tfidf,

    "ml/tfidf.pkl"

)

print()

print("Model Saved Successfully.")