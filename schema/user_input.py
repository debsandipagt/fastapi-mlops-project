# ================================
# 📦 IMPORT LIBRARIES
# ================================
from pydantic import BaseModel, Field, computed_field, field_validator  # WHY: Validation + feature engineering
from typing import Literal, Annotated           # WHY: Strict typing & controlled inputs

# ================================
# 🏙️ CITY DATA
# ================================

tier_1_cities = [
    "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai",
    "Kolkata", "Pune", "Ahmedabad"
]  # WHY: High-cost metro cities → higher premium impact

tier_2_cities = [
    "Lucknow", "Kanpur", "Jaipur", "Surat", "Chandigarh",
    "Indore", "Nagpur", "Bhopal", "Patna", "Coimbatore",
    "Kochi", "Visakhapatnam", "Vadodara", "Agra",
    "Varanasi", "Guwahati", "Mysuru", "Raipur",
    "Ranchi", "Amritsar"
]  # WHY: Mid-level cities → moderate impact


# ================================
# 📥 INPUT MODEL
# ================================

class UserInput(BaseModel):
    # WHY: Defines schema → validates incoming request automatically

    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of user")]
    # WHY: Prevent invalid values like negative age or unrealistic values

    weight: Annotated[int, Field(..., gt=0, description="Weight in kg")]
    # WHY: Weight must be positive

    height: Annotated[float, Field(..., gt=0, lt=2.5, description="Height in meters")]
    # WHY: Prevent wrong units (like cm → 170 instead of 1.7)

    income_lpa: Annotated[float, Field(..., gt=0, description="Income in LPA")]
    # WHY: Income must be positive

    smoker: Annotated[bool, Field(..., description="Is user a smoker")]
    # WHY: Boolean simplifies logic (True/False)

    city: Annotated[str, Field(..., description="City name")]
    # WHY: Used for tier mapping

    occupation: Annotated[
        Literal['retired', 'freelancer', 'student', 'government_job',
                'business_owner', 'unemployed', 'private_job'],
        Field(..., description="Occupation of user")
    ]
    # WHY: Restricts input → avoids unexpected categories (model consistency)

    # ================================
    # 🧹 VALIDATOR
    # ================================

    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        return v.strip().title()
    # WHY:
    # - Removes extra spaces
    # - Converts "guwahati" → "Guwahati"
    # - Ensures consistent matching with city lists

    # ================================
    # ⚙️ FEATURE ENGINEERING
    # ================================

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)
    # WHY:
    # - BMI is not given → derived
    # - Important health indicator for insurance risk

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
    # WHY:
    # - Combines smoking + BMI → stronger feature
    # - Improves model prediction quality

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 65:
            return "middle_aged"
        else:
            return "senior"
    # WHY:
    # - Converts continuous age → categories
    # - Reduces noise, improves model performance

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
    # WHY:
    # - Reduces high-cardinality feature (many cities → 3 tiers)
    # - Helps model generalize better
