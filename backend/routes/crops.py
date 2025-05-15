from fastapi import APIRouter, HTTPException
import joblib
import pandas as pd
from ..services.planner import CropPlanner

router = APIRouter()

model = joblib.load("backend/ml/crop_model.pkl")
encoders = joblib.load("backend/ml/label_encoders.pkl")
planner = CropPlanner("data/crop_lifecycle.xlsx")

@router.post("/recommend_crop")
def recommend_crop(input_data: dict):
    try:
        df = pd.DataFrame([input_data])
        for col in ["Soil Type"]:
            df[col] = encoders[col].transform(df[col])
        prediction = model.predict(df)[0]
        crop_name = encoders["Crop Type"].inverse_transform([prediction])[0]
        plan = planner.get_plan(crop_name)
        return {"recommended_crop": crop_name, "lifecycle_plan": plan}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
