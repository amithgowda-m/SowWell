from fastapi import APIRouter
from pydantic import BaseModel
import joblib
import numpy as np
import json

router = APIRouter()

# Load model and encoders
clf = joblib.load("ml/crop_model.pkl")
label_encoders = joblib.load("ml/label_encoders.pkl")

# Load crop lifecycle steps
with open("data/crop_lifecycle.json") as f:
    crop_lifecycle = json.load(f)

class CropInput(BaseModel):
    temperature: float
    humidity: float
    moisture: float
    soil_type: str
    n: float
    p: float
    k: float

@router.post("/recommend-crop/")
def recommend_crop(data: CropInput):
    # Encode soil type
    soil_encoded = label_encoders['Soil Type'].transform([data.soil_type])[0]
    # Prepare input
    X = np.array([[data.temperature, data.humidity, data.moisture, soil_encoded, data.n, data.p, data.k]])
    # Predict crop
    crop_encoded = clf.predict(X)[0]
    crop_name = label_encoders['Crop Type'].inverse_transform([crop_encoded])[0]
    # Predict fertilizer (if needed, or use logic)
    # For demo, get most common fertilizer for that crop from training data
    fertilizer_encoded = df[df['Crop Type'] == crop_encoded]['Fertilizer Name'].mode()[0]
    fertilizer_name = label_encoders['Fertilizer Name'].inverse_transform([fertilizer_encoded])[0]
    # Lifecycle steps
    lifecycle = crop_lifecycle.get(crop_name, [])
    return {
        "crop": crop_name,
        "fertilizer": fertilizer_name,
        "lifecycle": lifecycle,
        "why_fertilizer": f"{fertilizer_name} is recommended based on soil and crop requirements."
    }
