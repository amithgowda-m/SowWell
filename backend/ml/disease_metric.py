import matplotlib.pyplot as plt
import numpy as np

# List of all classes from the provided data
classes = [
    'Apple_Apple_scab', 'Apple_Black_rot', 'Apple_Cedar_apple_rust', 'Apple_healthy',
    'Blueberry_healthy', 'Cherry_Powdery_mildew', 'Cherry_healthy',
    'Corn_Cercospora_leaf_spot', 'Corn_Common_rust', 'Corn_Northern_Leaf_Blight', 'Corn_healthy',
    'Grape_Black_rot', 'Grape_Esca', 'Grape_Leaf_blight', 'Grape_healthy',
    'Orange_Haunglongbing', 'Peach_Bacterial_spot', 'Peach_healthy',
    'Pepper_Bacterial_spot', 'Pepper_healthy', 'Potato_Early_blight', 'Potato_Late_blight',
    'Potato_healthy', 'Raspberry_healthy', 'Soybean_healthy', 'Squash_Powdery_mildew',
    'Strawberry_Leaf_scorch', 'Strawberry_healthy', 'Tomato_Bacterial_spot',
    'Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites', 'Tomato_Target_Spot',
    'Tomato_Yellow_Leaf_Curl', 'Tomato_mosaic_virus', 'Tomato_healthy'
]

# Metrics for each class (Precision, Recall, F1-Score) extracted from the provided data
precision = [
    0.98, 0.99, 0.99, 0.98, 0.99, 1.00, 1.00, 0.96, 1.00, 0.96, 0.99,
    0.99, 0.98, 1.00, 1.00, 1.00, 0.99, 0.99, 0.98, 0.98, 1.00, 0.97,
    0.99, 1.00, 0.99, 1.00, 1.00, 1.00, 0.96, 0.90, 0.92, 0.96,
    0.94, 0.94, 0.89, 0.98, 0.97, 0.97
]

recall = [
    0.98, 0.99, 1.00, 0.98, 1.00, 0.99, 0.99, 0.96, 1.00, 0.96, 1.00,
    0.98, 0.99, 1.00, 1.00, 1.00, 0.99, 0.99, 0.97, 0.99, 0.99, 0.96,
    0.98, 1.00, 1.00, 1.00, 1.00, 1.00, 0.97, 0.88, 0.92, 0.95,
    0.93, 0.94, 0.91, 0.98, 0.99, 0.99
]

f1_score = [
    0.98, 0.99, 0.99, 0.98, 0.99, 1.00, 1.00, 0.96, 1.00, 0.96, 1.00,
    0.99, 0.99, 1.00, 1.00, 1.00, 0.99, 0.99, 0.98, 0.99, 1.00, 0.97,
    0.98, 1.00, 0.99, 1.00, 1.00, 1.00, 0.96, 0.89, 0.92, 0.96,
    0.94, 0.94, 0.90, 0.98, 0.98, 0.98
]

# Set the width of the bars
bar_width = 0.25

# Set position of bar on X axis
r1 = np.arange(len(classes))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]

# Create the bar plot with a larger figure size for readability
plt.figure(figsize=(20, 8))
plt.bar(r1, precision, color='b', width=bar_width, edgecolor='grey', label='Precision')
plt.bar(r2, recall, color='g', width=bar_width, edgecolor='grey', label='Recall')
plt.bar(r3, f1_score, color='r', width=bar_width, edgecolor='grey', label='F1-Score')

# Add labels and title
plt.xlabel('Classes', fontweight='bold')
plt.ylabel('Scores', fontweight='bold')
plt.xticks([r + bar_width for r in range(len(classes))], classes, rotation=90, ha='center')
plt.title('Performance Metrics for All Plant Disease Classifications')
plt.legend()

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Display the plot
plt.show()
