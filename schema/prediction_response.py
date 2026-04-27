from pydantic import BaseModel, Field
from typing import Annotated, Literal, Dict

class PredictionResponse(BaseModel):

    predicted_catagory: Annotated[str, Field(..., description="The predicted insurance premium catagory", examples=["High"])]
    confidence:  Annotated[float, Field(..., description="Models confidence score for the predicted class range (0 to 1)", examples=[0.833])]
    class_probabilities: Annotated[Dict[str, float], Field(..., description="Probability distribution accross all probable class", examples=[{"Low": 0.01, "Medium": 0.48, "High": 0.97}])]