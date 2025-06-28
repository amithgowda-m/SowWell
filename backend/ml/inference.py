import torch
from torchvision import models, transforms
from PIL import Image
import json
from pathlib import Path

# Define device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load prevention data
BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
PREVENTION_DATA_PATH = BASE_DIR / "data" / "disease_prevention.json"

try:
    with open(PREVENTION_DATA_PATH, "r", encoding="utf-8") as f:
        disease_prevention = json.load(f)
    print(f"✅ Prevention data loaded from {PREVENTION_DATA_PATH}")
except FileNotFoundError:
    raise FileNotFoundError(f"Prevention JSON file not found at {PREVENTION_DATA_PATH}")
except UnicodeDecodeError as e:
    raise RuntimeError(f"Encoding error in JSON file: {e}. Make sure it's saved as UTF-8")

def get_prevention_steps(disease_name, lang="en"):
    """
    Returns prevention steps in the specified language.
    Supported: 'en' (English), 'kn' (Kannada)
    """
    entry = disease_prevention.get(disease_name, {})
    if lang == "kn":
        return entry.get("prevention_kn", ["ಯಾವುದೇ ತಡೆಗಟ್ಟುವ ಕ್ರಮಗಳ ಮಾಹಿತಿಯಿಲ್ಲ."])
    else:
        return entry.get("prevention_en", ["No prevention steps found."])

# Correct class names (from your classification report)
class_names = [
    "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
    "Blueberry___healthy", "Cherry_(including_sour)___Powdery_mildew", "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot", "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___healthy", "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)", "Peach___Bacterial_spot", "Peach___healthy",
    "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy", "Potato___Early_blight",
    "Potato___Late_blight", "Potato___healthy", "Raspberry___healthy", "Soybean___healthy",
    "Squash___Powdery_mildew", "Strawberry___Leaf_scorch", "Strawberry___healthy",
    "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight", "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites Two-spotted_spider_mite", "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus", "Tomato___healthy"
]

# Image transform pipeline
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

# Load trained model
def load_model(model_path="ml/trained_plant_disease_model.pth"):
    try:
        model = models.resnet50(weights=None)
        model.fc = torch.nn.Linear(model.fc.in_features, len(class_names))
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.to(device)
        model.eval()
        print("✅ Model loaded successfully.")
        return model
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return None

# Predict disease from PIL image
def predict_image(image, model, lang="en"):
    try:
        image_tensor = transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            output = model(image_tensor)

        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        predicted_index = torch.argmax(probabilities).item()
        confidence = probabilities[predicted_index].item()

        disease_name = class_names[predicted_index]
        prevention_steps = get_prevention_steps(disease_name, lang=lang)

        return {
            "disease": disease_name,
            "confidence": round(confidence, 4),
            "prevention_steps": prevention_steps
        }

    except Exception as e:
        return {"error": str(e)}
