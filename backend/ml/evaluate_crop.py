# evaluate_model.py

from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Define or load y_test and y_pred before using them
# Example: load from files or generate from your model
# y_test = ...
# y_pred = ...

# Generate confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Save as CSV
pd.DataFrame(cm, index=label_encoders["Crop Type"].classes_, columns=label_encoders["Crop Type"].classes_).to_csv("confusion_matrix.csv")

# Save as image
def save_confusion_matrix_as_image(cm, classes, filename):
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=classes, yticklabels=classes)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

save_confusion_matrix_as_image(cm, label_encoders["Crop Type"].classes_, "confusion_matrix.png")