import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("../data/crop_data.csv")
df.dropna(inplace=True)

# Encode categorical columns
label_encoders = {}
categorical_columns = ['Soil Type', 'Fertilizer Name', 'Crop Type']
for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Features and label
X = df.drop("Fertilizer Name", axis=1)
y = df["Fertilizer Name"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(classification_report(
    y_test, y_pred, target_names=label_encoders["Fertilizer Name"].classes_))

# Save model and encoders
joblib.dump(clf, "fertilizer_model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")

# Save classification report as image
def save_classification_report_as_image(report, filename):
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    report_df = pd.DataFrame(report).T
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(report_df.iloc[:-3, :-1], annot=True, fmt=".2f", cmap="Blues", cbar=False)
    plt.title("Classification Report")
    plt.savefig(filename, bbox_inches="tight", dpi=300)
    plt.close()

save_classification_report_as_image(classification_report(y_test, y_pred, output_dict=True), "fertilizer_classification_report.png")

# Save confusion matrix as image
def save_confusion_matrix_as_image(cm, classes, filename):
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=classes, yticklabels=classes)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

cm = confusion_matrix(y_test, y_pred)
save_confusion_matrix_as_image(cm, label_encoders["Fertilizer Name"].classes_, "fertilizer_confusion_matrix.png")

# Feature importance
def save_feature_importance_as_image(importances, feature_names, filename):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=importances, y=feature_names, palette="viridis")
    plt.title("Feature Importances")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

importances = clf.feature_importances_
feature_names = X.columns.tolist()
save_feature_importance_as_image(importances, feature_names, "fertilizer_feature_importance.png")