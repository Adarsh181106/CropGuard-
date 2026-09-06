from flask import Flask, request, jsonify, send_from_directory
from predict import predict
from translate import get_localized_result, translate_text
from PIL import Image
import numpy as np
import cv2
import base64
import io

app = Flask(__name__, static_folder="static")

def encode_image_to_base64(image_np):
    """Converts a numpy image (like our heatmap) into a string the browser can display directly."""
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    success, buffer = cv2.imencode(".png", image_bgr)
    encoded = base64.b64encode(buffer).decode("utf-8")
    return f"data:image/png;base64,{encoded}"

@app.route("/")
def serve_frontend():
    return send_from_directory("static", "index.html")

@app.route("/predict", methods=["POST"])
def handle_predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]
    language = request.form.get("language", "en")  # defaults to English if not sent

    image = Image.open(image_file.stream)
    result = predict(image)

    if result is None:
        message = translate_text(
            "This doesn't look like a plant leaf. Please upload a clear photo of a leaf.",
            language
        )
        return jsonify({"error": "not_a_leaf", "message": message}), 200

    raw_label, confidence_pct, severity_pct, heatmap_np = result

    disease_name, treatment = get_localized_result(raw_label, language)
    heatmap_data_url = encode_image_to_base64(heatmap_np)

    return jsonify({
        "disease": disease_name,
        "confidence": confidence_pct,
        "severity": severity_pct,
        "treatment": treatment,
        "heatmap": heatmap_data_url,
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)