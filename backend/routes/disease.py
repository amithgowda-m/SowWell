# backend/routes/disease.py

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from ml.inference import load_model, predict_image  # Adjusted import path
from PIL import Image
import io

router = APIRouter(prefix="/api/disease", tags=["Disease Detection"])

# Load once at startup
model_path = "ml/trained_plant_disease_model.pth"
model = load_model(model_path=model_path)

@router.post("/predict")
async def predict_disease(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        return JSONResponse(status_code=400, content={"error": "Invalid file type. Please upload an image."})

    try:
        # Read and open image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        # Run inference
        result = predict_image(image, model)

        if "error" in result:
            return JSONResponse(status_code=500, content=result)

        return result

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})