from flask import Flask, request, jsonify
import cv2
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Load AI Model (Replace with your own)
model = tf.keras.models.load_model("your_model.h5")

@app.route('/analyze', methods=['POST'])
def analyze():
    img_data = request.data
    np_img = np.frombuffer(img_data, np.uint8)
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # Preprocess for AI Model
    image = cv2.resize(image, (224, 224)) / 255.0
    image = np.expand_dims(image, axis=0)

    # Get AI Prediction
    prediction = model.predict(image)
    result = {"prediction": prediction.tolist()}

    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
