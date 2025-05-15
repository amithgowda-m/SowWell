import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load dataset
df = pd.read_csv("../../data/crop_data.csv")

# Drop missing values
df.dropna(inplace=True)

# Encode categorical columns
label_encoders = {}
categorical_columns = ['Soil Type', 'Fertilizer Name', 'Crop Type']
for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Features and label
X = df.drop("Crop Type", axis=1)
y = df["Crop Type"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(classification_report(
    y_test, y_pred, target_names=label_encoders["Crop Type"].classes_))

# Save model and encoders
joblib.dump(clf, "crop_model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")
