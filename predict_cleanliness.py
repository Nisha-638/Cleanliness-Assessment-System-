import os
import cv2
import numpy as np
from ultralytics import YOLO

# ---------------- CONFIG ----------------
MODEL_PATH = "runs/segment/runs/segment/sanitation_seg/weights/best.pt"
SOURCE = "test_images"
OUTPUT_LABELS = "predicted_txt"

os.makedirs(OUTPUT_LABELS, exist_ok=True)

# ---------------- LOAD MODEL ----------------
model = YOLO(MODEL_PATH)

results = model.predict(
    source=SOURCE,
    imgsz=640,
    conf=0.3,
    save=False
)

# ---------------- PROCESS EACH IMAGE ----------------
for r in results:

    image_path = r.path
    image_name = os.path.basename(image_path)
    base_name = os.path.splitext(image_name)[0]

    label_path = os.path.join(OUTPUT_LABELS, base_name + ".txt")
    f = open(label_path, "w")

    if r.masks is None:
        f.close()
        continue

    h, w = r.orig_shape
    masks_xy = r.masks.xy  # polygon points (pixel format)
    classes = r.boxes.cls.cpu().numpy().astype(int)

    # For each detected object
    for cls, polygon in zip(classes, masks_xy):

        # Normalize polygon points
        normalized_points = []
        for x, y in polygon:
            x_norm = x / w
            y_norm = y / h
            normalized_points.append(f"{x_norm:.6f}")
            normalized_points.append(f"{y_norm:.6f}")

        line = str(cls) + " " + " ".join(normalized_points) + "\n"
        f.write(line)

    f.close()

print("✅ Segmentation TXT files saved in:", OUTPUT_LABELS)
