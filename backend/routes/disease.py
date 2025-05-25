from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from PIL import Image
from io import BytesIO
import json

router = APIRouter()

# Load model once at startup
try:
    model = tf.keras.models.load_model("ml/trained_model.h5")
    print("✅ Disease model loaded successfully.")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    model = None

# Example class names (ensure this matches your model's training output)
class_names = [
    "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
    "Blueberry___healthy", "Cherry_(including_sour)___Powdery_mildew", "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot", "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___healthy", "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)", "Peach___Bacterial_spot", "Peach___healthy",
    "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy", "Potato___Early_blight",
    "Potato___Late_blight", "Potato___healthy", "Raspberry___healthy", "Soybean___healthy",
    "Squash___Powdery_mildew", "Strawberry___Leaf_scorch", "Strawberry___healthy", "Tomato___Bacterial_spot",
    "Tomato___Early_blight", "Tomato___Late_blight", "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite", "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus", "Tomato___healthy"
]

# Dummy fallback guide data (replace with actual knowledge base if available)
disease_prevention_guide = {
    "Tomato___Bacterial_spot": {
        "prevention": [
            "Avoid overhead irrigation.",
            "Use disease-free seeds.",
            "Apply copper-based fungicides."
        ],
        "recommend_crop": "Tomato"
    },
    "Tomato___healthy": {
        "prevention": ["Maintain proper spacing.", "Fertilize regularly."],
        "recommend_crop": "Tomato"
    },
    # Add more diseases as needed
}

# Dummy crop lifecycle steps (replace with real data from your JSON file)
crop_lifecycle = {
    "Tomato": [
        "Germination: 5–10 days after planting.",
        "Vegetative Growth: 20–30 days.",
        "Flowering: 30–40 days.",
        "Fruiting: 50+ days."
    ]
}

@router.post("/predict-disease/")
async def predict_disease(file: UploadFile = File(...)):
    if model is None:
        return JSONResponse(status_code=500, content={"error": "Model not loaded."})

    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents)).convert("RGB").resize((128, 128))
        image_array = np.array(image) / 255.0  # Normalize to [0,1]
        image_batch = np.expand_dims(image_array, axis=0)

        prediction = model.predict(image_batch)
        result_index = int(np.argmax(prediction))
        disease_name = class_names[result_index]

        response = {
            "disease": disease_name,
            "prevention_steps": [],
            "recommended_crop": None,
            "crop_lifecycle": []
        }

        # Optional: Provide recommendations based on disease
        if disease_name in disease_prevention_guide:
            info = disease_prevention_guide[disease_name]
            response["prevention_steps"] = info.get("prevention", [])
            response["recommended_crop"] = info.get("recommend_crop", None)
            response["crop_lifecycle"] = crop_lifecycle.get(info.get("recommend_crop", ""), [])

        return JSONResponse(content=response)

    except Exception as e:
        print(f"🚨 Error during prediction: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )