# evaluate_model.py

import os
import torch
from torchvision import transforms, datasets, models
from torch.utils.data import DataLoader
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
import matplotlib.pyplot as plt
import pandas as pd

# Device configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "trained_plant_disease_model.pth")
data_dir = os.path.join(base_dir, "..", "data", "Disease", "Valid")

# Transforms
image_size = 224
transform = transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Dataset and DataLoader
dataset = datasets.ImageFolder(data_dir, transform)
dataloader = DataLoader(dataset, batch_size=32, shuffle=False)
class_names = dataset.classes

# Load model
model = models.resnet50(weights=None)
num_ftrs = model.fc.in_features
model.fc = torch.nn.Linear(num_ftrs, len(class_names))
model.load_state_dict(torch.load(model_path, map_location=device))
model = model.to(device)
model.eval()

# Inference
all_preds = []
all_labels = []

with torch.no_grad():
    for inputs, labels in dataloader:
        inputs = inputs.to(device)
        labels = labels.to(device)
        outputs = model(inputs)
        _, preds = torch.max(outputs, 1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

# Classification Report
print("\nClassification Report:")
report = classification_report(all_labels, all_preds, target_names=class_names, output_dict=True)
print(classification_report(all_labels, all_preds, target_names=class_names))

# Save classification report
report_df = pd.DataFrame(report).transpose()
report_df.to_csv("classification_report.csv", index=True)
print("Saved classification_report.csv")

# Confusion Matrix
cm = confusion_matrix(all_labels, all_preds)
cm_df = pd.DataFrame(cm, index=class_names, columns=class_names)
cm_df.to_csv("confusion_matrix.csv")
print("Saved confusion_matrix.csv")

# High-Resolution Confusion Matrix Image
fig, ax = plt.subplots(figsize=(14, 12))  # Larger figure size
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
disp.plot(cmap=plt.cm.Blues, xticks_rotation=45, ax=ax, values_format='d')  # Integer format

# Improve readability
plt.title("Confusion Matrix", fontsize=18)
plt.xlabel("Predicted Label", fontsize=14)
plt.ylabel("True Label", fontsize=14)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()

# Save high-quality PNG
plt.savefig("confusion_matrix.png", dpi=600)  # High DPI for clear print-quality image
print("Saved high-resolution confusion_matrix.png")

plt.show()
