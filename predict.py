import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import json
import numpy as np
import cv2
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image

# --- Load model and classes once, when the app starts ---
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
def is_likely_leaf(image_np):
    """
    Heuristic, not a trained classifier — narrowed to target actual leaf-green
    hues and exclude low-saturation neutral tones (skin, beige/tan fabric, walls).
    Still imperfect by nature of being color-only; a production version would
    use a dedicated leaf/not-leaf classifier.
    """
    hsv = cv2.cvtColor(image_np, cv2.COLOR_RGB2HSV)
    plant_mask = cv2.inRange(hsv, np.array([30, 45, 20]), np.array([95, 255, 220]))
    plant_ratio = np.sum(plant_mask > 0) / (image_np.shape[0] * image_np.shape[1])
    return plant_ratio > 0.12
def get_gradcam_overlay(image_np, input_tensor, predicted_idx):
    target_layers = [model.features[-1]]
    cam = GradCAM(model=model, target_layers=target_layers)
    targets = [ClassifierOutputTarget(predicted_idx)]
    grayscale_cam = cam(input_tensor=input_tensor, targets=targets)[0]
    resized_image = cv2.resize(image_np, (224, 224))
    visualization = show_cam_on_image(resized_image / 255.0, grayscale_cam, use_rgb=True)
    return visualization

def predict(image):
    """
    Returns RAW values (not formatted strings) so the backend (app.py)
    can format and translate them however it needs to.
    """
    image = image.convert("RGB")
    image_np = np.array(image)
    if not is_likely_leaf(image_np):
        return None
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(input_tensor)
        probs = torch.softmax(outputs, dim=1)
        confidence, predicted_idx = torch.max(probs, 1)

    label = class_names[predicted_idx.item()]              # e.g. "Tomato___Late_blight"
    confidence_pct = round(confidence.item() * 100, 1)       # e.g. 76.5
    severity_pct = estimate_severity(image_np)                # e.g. 81.0
    heatmap_np = get_gradcam_overlay(image_np, input_tensor, predicted_idx.item())

    return label, confidence_pct, severity_pct, heatmap_np