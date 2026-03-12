# from ultralytics import YOLO
# import cv2
# import numpy as np
# import os

# # Load segmentation model
# model = YOLO("C:/Users/Ayushi/Desktop/sanitation_yolo_project/runs/segment/runs/segment/sanitation_seg/weights/best.pt")

# # Input images
# SOURCE = "test_images"

# # Output folder
# SAVE_DIR = "cleanliness_results"
# os.makedirs(SAVE_DIR, exist_ok=True)


# def cleanliness_score(mask, image):
#     h, w = image.shape[:2]

#     mask = cv2.resize(mask, (w, h))
#     mask = (mask * 255).astype(np.uint8)

#     masked = cv2.bitwise_and(image, image, mask=mask)

#     gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
#     pixels = gray[mask == 255]

#     if len(pixels) == 0:
#         return "Unknown"

#     mean = np.mean(pixels)
#     std = np.std(pixels)

#     if mean > 170 and std < 40:
#         return "Good"
#     elif mean > 120:
#         return "Average"
#     else:
#         return "Bad"

# for img_name in os.listdir(SOURCE):
#     if not img_name.lower().endswith((".jpg", ".png", ".jpeg")):
#         continue

#     img_path = os.path.join(SOURCE, img_name)
#     image = cv2.imread(img_path)

#     results = model.predict(source=img_path, conf=0.25, save=False)

#     for r in results:
#         if r.masks is None:
#             continue

#         for i, mask in enumerate(r.masks.data):
#             cls = int(r.boxes.cls[i])
#             conf = float(r.boxes.conf[i])
#             name = model.names[cls]

#             mask_np = mask.cpu().numpy()
#             status = cleanliness_score(mask_np, image)

#             box = r.boxes.xyxy[i].cpu().numpy().astype(int)
#             x1, y1, x2, y2 = box

#             if status == "Good":
#                 color = (0, 255, 0)
#             elif status == "Average":
#                 color = (0, 255, 255)
#             else:
#                 color = (0, 0, 255)

#             cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
#             cv2.putText(image, f"{name} {status} {conf:.2f}",
#                         (x1, y1 - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

#     cv2.imwrite(os.path.join(SAVE_DIR, img_name), image)

# print("✅ Cleanliness results saved in:", SAVE_DIR)
import os
import cv2
import numpy as np
from ultralytics import YOLO

# ---------------- CONFIG ----------------
MODEL_PATH = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/runs/segment/runs/segment/sanitation_seg/weights/best.pt"
SOURCE = "test_images"
SAVE_DIR = "cleanliness_results"
CONF = 0.3

os.makedirs(SAVE_DIR, exist_ok=True)

# ---------------- LOAD MODEL ----------------
model = YOLO(MODEL_PATH)

# ---------------- CLEANLINESS LOGIC ----------------
def cleanliness_score(mask, image):
    h, w = image.shape[:2]

    mask = cv2.resize(mask, (w, h))
    mask = (mask > 0.5).astype(np.uint8) * 255

    masked = cv2.bitwise_and(image, image, mask=mask)

    gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    dirt_ratio = np.sum(edges > 0) / np.sum(mask > 0)

    if dirt_ratio < 0.05:
        return "Good"
    elif dirt_ratio < 0.12:
        return "Average"
    else:
        return "Bad"

# ---------------- PROCESS ----------------
for img_name in os.listdir(SOURCE):
    if not img_name.lower().endswith((".jpg", ".png", ".jpeg")):
        continue

    img_path = os.path.join(SOURCE, img_name)
    image = cv2.imread(img_path)
    h, w = image.shape[:2]

    results = model.predict(img_path, conf=CONF, save=False)

    for r in results:
        if r.masks is None:
            continue

        masks = r.masks.data.cpu().numpy()
        boxes = r.boxes

        for i, mask in enumerate(masks):
            cls = int(boxes.cls[i])
            conf = float(boxes.conf[i])
            name = model.names[cls]

            status = cleanliness_score(mask, image)

            mask = cv2.resize(mask, (w, h))
            mask = (mask > 0.5).astype(np.uint8)

            np.random.seed(cls)
            color = np.random.randint(0, 255, 3).tolist()

            overlay = image.copy()
            overlay[mask == 1] = overlay[mask == 1] * 0.4 + np.array(color) * 0.6
            image = overlay.astype(np.uint8)

            x1, y1, x2, y2 = map(int, boxes.xyxy[i])

            cv2.rectangle(image, (x1, y1), (x2, y2), color, 3)

            label = f"{name} {conf:.2f} {status}"

            cv2.putText(
                image,
                label,
                (x1, max(y1 - 15, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                color,
                3,
                cv2.LINE_AA,
            )

    image = cv2.resize(image, None, fx=1.3, fy=1.3)
    cv2.imwrite(os.path.join(SAVE_DIR, img_name), image)

print("✅ Done! Check folder:", SAVE_DIR)
