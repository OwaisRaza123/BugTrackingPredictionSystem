import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# ==========================
# Load Dataset
# ==========================

data = pd.read_csv("dataset/resolution_processed.csv")

# Remove empty rows
data = data.dropna(subset=["Clean_Text"])

# Convert to string
data["Clean_Text"] = data["Clean_Text"].astype(str)

print("Dataset Shape :", data.shape)

# ==========================
# Features & Target
# ==========================

X = data["Clean_Text"]

# Target Column
y = data["Fixing_time"]

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

model = LinearRegression()

model.fit(X_train, y_train)

prediction = model.predict(X_test)

mae = mean_absolute_error(

    y_test,

    prediction

)

print("\nModel Trained Successfully")

print("Mean Absolute Error :", round(mae,2), "days")


# ==========================
# Save Model
# ==========================

pickle.dump(

    model,

    open("ml/resolution_model.pkl", "wb")

)

pickle.dump(

    tfidf,

    open("ml/resolution_tfidf.pkl", "wb")

)

print("\nResolution Model Saved Successfully")