import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing import image_dataset_from_directory
import json

# Set parameters
batch_size = 32
img_height = 300
img_width = 300
data_dir = "/home/imdavid/workplace/dooropener/src/Dataset/"
code_path = "/home/imdavid/workplace/dooropener/src/"

def preprocess_image(image, target_size):
    # Resize the image to fit within the target size while maintaining aspect ratio
    image = tf.image.resize_with_pad(image, target_size[0], target_size[1])
    return image

# Load dataset
train_dataset = image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),  # This will still resize to 180x180
    batch_size=batch_size
)

# Access class names before mapping
class_names = train_dataset.class_names
print(class_names)

# Apply preprocessing
train_dataset = train_dataset.map(lambda x, y: (preprocess_image(x, (img_height, img_width)), y))

validation_dataset = image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

validation_dataset = validation_dataset.map(lambda x, y: (preprocess_image(x, (img_height, img_width)), y))

# Define the model
model = models.Sequential([
    layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(class_names), activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

epochs = 6  # You can adjust the number of epochs based on your needs

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=epochs
)

# Evaluate the model
val_loss, val_acc = model.evaluate(validation_dataset)
print(f"Validation Accuracy: {val_acc:.2f}")
print(f"Validation Loss: {val_loss:.2f}")

model.save(f'{code_path}dog_detection_model.keras')

# Save the class names to a JSON file
class_names_path = f'{code_path}class_names.json'
with open(class_names_path, 'w') as f:
    json.dump(class_names, f)
