import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the pre-trained Food101 model
model = MobileNetV2(weights='imagenet', include_top=True)

# Load and preprocess the input image
img_path = './examples/paris2.jpg'
img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

# Use the model to make a prediction on the input image
preds = model.predict(x)
# Get the top 5 predictions
top_preds = tf.keras.applications.imagenet_utils.decode_predictions(preds, top=5)[0]

# Print the top 5 predictions (class name, class ID, and prediction score)
for pred in top_preds:
    print(pred[0], pred[1], pred[2])
