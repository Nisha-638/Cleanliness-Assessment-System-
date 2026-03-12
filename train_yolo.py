from ultralytics import YOLO

model = YOLO("yolov8n-seg.pt")

model.train(
    data="data.yaml",
    epochs=30,
    imgsz=640,
    batch=8,
    project="runs/segment",
    name="sanitation_seg"
)
