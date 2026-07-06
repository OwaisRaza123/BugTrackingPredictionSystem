import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Algorithms
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier

# ==========================
# Load Dataset
# ==========================

data = pd.read_csv("dataset/severity_processed.csv")

# Remove empty rows
data = data.dropna(subset=["Clean_Text"])

data["Clean_Text"] = data["Clean_Text"].astype(str)

# Features
X = data["Clean_Text"]

# Target
y = data["Severity"]

# TF-IDF

tfidf = TfidfVectorizer(max_features=5000)

X = tfidf.fit_transform(X)

# Train Test Split

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42

)

# ==========================
# Models
# ==========================

models = {

    "Naive Bayes": MultinomialNB(),

    "Logistic Regression": LogisticRegression(max_iter=1000),

    "Linear SVM": LinearSVC(),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

}

print("\n==============================")
print("Severity Prediction Accuracy")
print("==============================\n")

best_accuracy = 0
best_model = ""

for name, model in models.items():

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    accuracy = accuracy_score(y_test, prediction)

    print(f"{name:25} : {accuracy*100:.2f}%")

    if accuracy > best_accuracy:

        best_accuracy = accuracy

        best_model = name

print("\n==============================")
print("Best Model :", best_model)
print("Accuracy   :", round(best_accuracy*100,2),"%")
print("==============================")