import pandas as pd
import re
import nltk

from nltk.corpus import stopwords

# Download stopwords (only first time)
nltk.download('stopwords')

# ==========================
# Load Clean Dataset
# ==========================

severity = pd.read_csv("dataset/severity_clean.csv")

# ==========================
# Stopwords
# ==========================

stop_words = set(stopwords.words('english'))

# ==========================
# Clean Function
# ==========================

def clean_text(text):

    text = str(text).lower()

    # Remove numbers
    text = re.sub(r'\d+', '', text)

    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove stopwords
    words = text.split()

    words = [
        word
        for word in words
        if word not in stop_words
    ]

    return " ".join(words)

# ==========================
# Apply Cleaning
# ==========================

severity["Clean_Text"] = severity["Description"].apply(clean_text)

print(severity[["Description", "Clean_Text"]].head())

# Save

severity.to_csv(
    "dataset/severity_processed.csv",
    index=False
)

print("\nText preprocessing completed successfully.")