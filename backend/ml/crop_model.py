import joblib
import pandas as pd
import os

# Load model and label encoders once
model_path = os.path.join(os.path.dirname(__file__), "crop_model.pkl")
encoder_path = os.path.join(os.path.dirname(__file__), "label_encoders.pkl")

model = joblib.load(model_path)
label_encoders = joblib.load(encoder_path)

def predict_crop(input_data: dict) -> str:
    try:
        # Encode categorical features
        for col in ['Soil Type', 'Fertilizer Name']:
            le = label_encoders[col]
            input_data[col] = le.transform([input_data[col]])[0]

        # Create DataFrame
        df = pd.DataFrame([input_data])

        # Predict
        pred = model.predict(df)[0]

        # Decode predicted label
        crop_label = label_encoders['Crop Type'].inverse_transform([pred])[0]
        return crop_label
    except Exception as e:
        raise ValueError(f"Error in prediction pipeline: {e}")
