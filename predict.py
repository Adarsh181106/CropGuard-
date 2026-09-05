import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import json
import numpy as np
import cv2

# --- Load model and classes once, when the app starts (not on every photo) ---
with open("model/classes.json") as f:
    class_names = json.load(f)

model = models.mobilenet_v2(weights=None)
model.classifier[1] = nn.Sequential(
    nn.Dropout(0.2),
    nn.Linear(model.classifier[1].in_features, len(class_names))
)
model.load_state_dict(torch.load("model/cropguard_mobilenetv2.pth", map_location="cpu"))
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# --- Simple treatment lookup ---
def get_treatment(label):
    if "healthy" in label.lower():
        return "No treatment needed — plant looks healthy."
    return "Remove affected leaves, avoid overhead watering, and consult a local agricultural extension officer for a targeted fungicide/pesticide recommendation."

# --- Severity estimation (color-based heuristic, not a trained model) ---
def estimate_severity(image_np):
    hsv = cv2.cvtColor(image_np, cv2.COLOR_RGB2HSV)
    healthy_mask = cv2.inRange(hsv, np.array([25, 40, 40]), np.array([90, 255, 255]))
    leaf_mask = cv2.inRange(hsv, np.array([0, 20, 20]), np.array([180, 255, 255]))
    leaf_pixels = np.sum(leaf_mask > 0)
    healthy_pixels = np.sum(healthy_mask > 0)
    if leaf_pixels == 0:
        return 0.0
    diseased_pixels = leaf_pixels - healthy_pixels
    return round(max(0, (diseased_pixels / leaf_pixels) * 100), 1)

# --- Main function the web app will call ---
def predict(image):
    image = image.convert("RGB")
    image_np = np.array(image)
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(input_tensor)
        probs = torch.softmax(outputs, dim=1)
        confidence, predicted_idx = torch.max(probs, 1)

    label = class_names[predicted_idx.item()]
    confidence_pct = round(confidence.item() * 100, 1)
    severity_pct = estimate_severity(image_np)
    treatment = get_treatment(label)

    return label, f"{confidence_pct}%", f"{severity_pct}%", treatment