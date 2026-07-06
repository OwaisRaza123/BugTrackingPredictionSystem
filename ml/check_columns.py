import pickle

with open("ml/severity_model.pkl", "rb") as f:
    model = pickle.load(f)

print("Model Loaded Successfully")