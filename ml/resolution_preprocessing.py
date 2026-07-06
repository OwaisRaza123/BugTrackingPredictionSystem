import pandas as pd
import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download resources
nltk.download("stopwords")
nltk.download("wordnet")

# ==========================
# Load Dataset
# ==========================

data = pd.read_csv("dataset/resolution_clean.csv")

print("Original Shape :", data.shape)

# Keep required columns
data = data[["Description", "Fixing_time"]]

# Remove empty rows
data = data.dropna()

lemmatizer = WordNetLemmatizer()

stop_words = set(stopwords.words("english"))

# ==========================
# Text Cleaning
# ==========================

def clean_text(text):

    text = str(text).lower()

    text = re.sub(r'[^a-zA-Z ]', ' ', text)

    words = text.split()

    words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word not in stop_words
    ]

    return " ".join(words)

# Create Clean_Text

data["Clean_Text"] = data["Description"].apply(clean_text)

# Save Processed Dataset

data.to_csv(

    "dataset/resolution_processed.csv",

    index=False

)

print("\nResolution Dataset Processed Successfully")

print(data.head())