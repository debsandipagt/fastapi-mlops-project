
# ================================
# 📦 IMPORT LIBRARIES
# ================================
import pickle                                   # WHY: Load trained ML model
import os


# ================================
# 🤖 LOAD MODEL
# ================================

def load_model():
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
        return model
    # WHY: Load trained ML model once at startup → avoids reloading per request (efficient)