from fastapi import APIRouter, Request
from pydantic import BaseModel
import joblib
import numpy as np
import json

router = APIRouter()

# Load models and encoders
try:
    clf = joblib.load("ml/crop_model.pkl")
    print("✅ Crop model loaded successfully.")
except Exception as e:
    print(f"❌ Failed to load crop model: {e}")
    clf = None

try:
    fertilizer_clf = joblib.load("ml/fertilizer_model.pkl")
    print("✅ Fertilizer model loaded successfully.")
except Exception as e:
    print(f"❌ Failed to load fertilizer model: {e}")
    fertilizer_clf = None

try:
    label_encoders = joblib.load("ml/label_encoders.pkl")
    print("✅ Label encoders loaded successfully.")
except Exception as e:
    print(f"❌ Failed to load label encoders: {e}")
    label_encoders = {}

# Load lifecycle steps
try:
    with open("data/crop_lifecycle.json") as f:
        crop_lifecycle = json.load(f)
    print("✅ Crop lifecycle steps loaded successfully.")
except Exception as e:
    print(f"❌ Failed to load lifecycle steps: {e}")
    crop_lifecycle = {}

class CropInput(BaseModel):
    temperature: float
    humidity: float
    moisture: float
    soil_type: str
    n: float
    p: float
    k: float
    rainfall: float

@router.post("/recommend-crop/")
def recommend_crop(data: CropInput):
    try:
        if clf is None or fertilizer_clf is None:
            return {"error": "Required model not loaded."}

        if not label_encoders:
            return {"error": "Label encoders not loaded."}

        # Validate soil type
        if data.soil_type not in label_encoders['Soil Type'].classes_:
            return {"error": f"Unseen soil type: '{data.soil_type}'"}

        # Encode soil type
        soil_encoded = label_encoders['Soil Type'].transform([data.soil_type])[0]

        # Prepare input array with all 8 features
        X = np.array([
            [data.temperature, data.humidity, data.moisture, soil_encoded, data.n, data.p, data.k, data.rainfall]
        ])

        # Predict crop
        crop_encoded = clf.predict(X)[0]
        crop_name = label_encoders['Crop Type'].inverse_transform([crop_encoded])[0]

        # Predict fertilizer
        fertilizer_encoded = fertilizer_clf.predict(X)[0]
        fertilizer_name = label_encoders['Fertilizer Name'].inverse_transform([fertilizer_encoded])[0]

        # Get lifecycle steps
        lifecycle = crop_lifecycle.get(crop_name, [])

        return {
            "recommended_crop": crop_name,
            "fertilizer": fertilizer_name,
            "lifecycle": lifecycle,
            "why_fertilizer": f"{fertilizer_name} is recommended based on soil and crop requirements."
        }

    except Exception as e:
        print(f"🚨 Error during crop recommendation: {str(e)}")
        return {"error": str(e)}