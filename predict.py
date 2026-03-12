# from ultralytics import YOLO
# import cv2
# import os

# # Load trained model
# model = YOLO("runs/detect/sanitation_model/weights/best.pt")

# # Folder of test images
# SOURCE = "test_images"
# SAVE_DIR = "test_results"

# os.makedirs(SAVE_DIR, exist_ok=True)

# for img_name in os.listdir(SOURCE):
#     if img_name.lower().endswith((".jpg", ".png", ".jpeg")):
#         img_path = os.path.join(SOURCE, img_name)

#         results = model.predict(source=img_path, conf=0.25, save=False)

#         img = cv2.imread(img_path)

#         for r in results:
#             for box in r.boxes:
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 cls = int(box.cls[0])
#                 conf = float(box.conf[0])

#                 label = f"{model.names[cls]} {conf:.2f}"

#                 cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
#                 cv2.putText(img, label, (x1, y1-10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

#         cv2.imwrite(os.path.join(SAVE_DIR, img_name), img)

# print("✅ Testing done. Check folder:", SAVE_DIR)
from ultralytics import YOLO

# Load your trained model
model = YOLO(r"runs/segment/runs/segment/sanitation_seg/weights/best.pt")

# Predict
results = model.predict(
    source="test_images",   # folder or image path
    save=True,
    imgsz=640,
    conf=0.3,
    show_boxes=True,
    show_labels=True,
    show_conf=True
)
print(model.names)
print("✅ Prediction done. Check runs/segment/predict/")
