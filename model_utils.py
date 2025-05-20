# model_utils.py
import tensorflow as tf
from PIL import Image
import numpy as np

# Load the trained model (make sure this matches your notebook code)
model = tf.keras.models.load_model('plant_disease_model.h5')

# List of class labels in same order as model trained
class_labels = [
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    # ... add all your labels here
]

def preprocess_image(image_path):
    img = Image.open(image_path).resize((224, 224))  # Resize as per model input
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_disease(image_path):
    img = preprocess_image(image_path)
    preds = model.predict(img)
    class_index = np.argmax(preds)
    disease = class_labels[class_index]
    return disease
