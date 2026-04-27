import pandas as pd
from model.load_model import load_model

model = load_model()

class_labels = model.classes_.tolist()

def predict_output(user_input: dict):
    df = pd.DataFrame([user_input])

    predicted_class = model.predict(df)[0]
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities)

    class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))

    return {
        "predicted_catagory": predicted_class,
        "confidence": round(confidence, 4),
        "class_probabilities": class_probs
    }