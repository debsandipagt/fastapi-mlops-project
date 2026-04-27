
# ================================
# 📦 IMPORT LIBRARIES
# ================================
import pickle                                   # WHY: Load trained ML model


# ================================
# 🤖 LOAD MODEL
# ================================

def load_model():
    with open(r"E:\Tavishi_Mentorship_Program\19_CampusX_FasiAPI_and_pydantic-tutorial\Fast_api_project\model\model.pkl", "rb") as f:
        model = pickle.load(f)
        return model
    # WHY: Load trained ML model once at startup → avoids reloading per request (efficient)