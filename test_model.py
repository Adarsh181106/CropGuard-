import torch
from torchvision import models
import torch.nn as nn
import json

with open("model/classes.json") as f:
    class_names = json.load(f)

print(f"Number of classes: {len(class_names)}")
print(f"First few classes: {class_names[:3]}")

model = models.mobilenet_v2(weights=None)
model.classifier[1] = nn.Sequential(
    nn.Dropout(0.2),
    nn.Linear(model.classifier[1].in_features, len(class_names))
)

model.load_state_dict(torch.load("model/cropguard_mobilenetv2.pth", map_location="cpu"))
model.eval()

print("Model loaded successfully!")