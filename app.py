# ================================
# 📦 IMPORT LIBRARIES
# ================================

from fastapi import FastAPI                     # WHY: Framework to build high-performance APIs
from fastapi.responses import JSONResponse      # WHY: To return custom JSON responses with status codes
from schema.user_input import UserInput         # WHY: Load UserInput class
from model.load_model import load_model         # WHY: Load model function
from model.predict import predict_output
from schema.prediction_response import PredictionResponse

# ================================
# 🚀 FASTAPI APP
# ================================

app = FastAPI(
    title="Insurance Premium Prediction API",  # WHY: Helps in API documentation (/docs)
    description="Predict insurance premium category",
    version="1.0"
)

#=================================
# LOADING THE MODEL
#=================================
model = load_model()

# ================================
# 🏠 HOME API
# ================================

@app.get("/")
def home():
    return {"message": "Insurance premium prediction API"}
# WHY: Basic check → confirms API is running

# ================================
# ❤️ HEALTH CHECK (For machine readable)
# ================================

@app.get("/health")
def health_check():
    return {
        "app": "OK",
        "model_loaded": model is not None,
        "api": "OK"
    }
# WHY:
# - Used in production monitoring
# - Helps detect system failures quickly
# - Used by Cloud provider

# ================================
# 🎯 PREDICTION API
# ================================

@app.post("/predict", response_model=PredictionResponse)
def predict_premium(data: UserInput):

    input_data = {
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }
    # WHY:
    # - Model expects structured tabular data
    # - Even single input → must be DataFrame

    try:
        prediction = predict_output(input_data) # import prediction function
        # WHY:
        # - model.predict returns array → take first value

        return JSONResponse(
            status_code=200,
            content={"response": prediction}
    )
    # WHY:
    # - Consistent API response format
    # - Easy for frontend to consume
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))