import matplotlib.pyplot as plt

# Accuracy values from your screenshot
train_acc = [0.8648, 0.9510, 0.9640, 0.9732, 0.9768, 0.9826, 0.9834, 0.9882, 0.9892, 0.9890]
val_acc = [0.9468, 0.9594, 0.9679, 0.9689, 0.9712, 0.9745, 0.9765, 0.9771, 0.9786, 0.9772]

epochs = range(1, len(train_acc) + 1)

plt.plot(epochs, train_acc, 'r', marker='o', label='Train Accuracy')
plt.plot(epochs, val_acc, 'b', marker='o', label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Training and Validation Accuracy Over Epochs')
plt.grid(True)
plt.tight_layout()
plt.show()
