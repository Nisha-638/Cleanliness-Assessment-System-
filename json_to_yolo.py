# import os
# import json
# import cv2

# # ---------------- CONFIG ----------------
# JSON_DIR = r"labelme_jsons"
# IMG_DIR  = r"dataset/good_images"
# OUT_DIR = r"dataset/yolo_dataset/labels/train"


# CLASSES = [
#     "commode",
#     "washbasin",
#     "dustbin",
#     "aisle"
# ]

# os.makedirs(OUT_DIR, exist_ok=True)

# print("\n🔄 Converting LabelMe JSON → YOLO Seg format...\n")

# files = os.listdir(JSON_DIR)
# print("📄 Total files found:", len(files))

# count = 0
# skipped = 0

# for file in files:
#     print("🔎 Found:", file)

#     if not file.lower().endswith(".json"):
#         continue

#     json_path = os.path.join(JSON_DIR, file)

#     try:
#         with open(json_path, "r", encoding="utf-8") as f:
#             data = json.load(f)
#     except Exception as e:
#         print(f"❌ Cannot open {file}: {e}")
#         skipped += 1
#         continue

#     image_name = data.get("imagePath") or file.replace(".json", ".jpg")
#     img_path = os.path.join(IMG_DIR, os.path.basename(image_name))

#     if not os.path.exists(img_path):
#         print(f"⚠ Image missing:", img_path)
#         skipped += 1
#         continue

#     img = cv2.imread(img_path)
#     h, w = img.shape[:2]

#     txt_name = os.path.splitext(file)[0] + ".txt"
#     out_path = os.path.join(OUT_DIR, txt_name)

#     written = False

#     with open(out_path, "w") as out:
#         for shape in data.get("shapes", []):
#             label = shape.get("label")

#             if label not in CLASSES:
#                 continue

#             if shape.get("shape_type") != "polygon":
#                 continue

#             points = shape.get("points", [])
#             if len(points) < 3:
#                 continue

#             cls_id = CLASSES.index(label)

#             line = [str(cls_id)]
#             for x, y in points:
#                 line.append(f"{x / w:.6f}")
#                 line.append(f"{y / h:.6f}")

#             out.write(" ".join(line) + "\n")
#             written = True

#     if written:
#         count += 1
#         print(f"✅ Converted:", file)
#     else:
#         skipped += 1
#         print(f"⚠ No valid labels:", file)


# print("\n---------- DONE ----------")
# print("Converted :", count)
# print("Skipped   :", skipped)
import os
import json
import cv2

# ---------------- CONFIG ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JSON_DIR = os.path.join(BASE_DIR, "labelme_jsons")
IMG_DIR  = os.path.join(BASE_DIR, "raw_images")
OUT_DIR  = os.path.join(BASE_DIR, "yolo_dataset", "labels", "all")

CLASSES = [
    "commode",
    "washbasin",
    "dustbin",
    "aisle",
    "toilet_floor"
]

os.makedirs(OUT_DIR, exist_ok=True)

print("\n🔄 Converting LabelMe JSON → YOLOv8 Segmentation...\n")

files = os.listdir(JSON_DIR)
print("📄 Total JSON files found:", len(files))

count = 0
skipped = 0

for file in files:
    if not file.lower().endswith(".json"):
        continue

    json_path = os.path.join(JSON_DIR, file)

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Cannot open {file}: {e}")
        skipped += 1
        continue

    image_name = data.get("imagePath") or file.replace(".json", ".jpg")
    img_path = os.path.join(IMG_DIR, os.path.basename(image_name))

    if not os.path.exists(img_path):
        print(f"⚠ Image missing:", img_path)
        skipped += 1
        continue

    img = cv2.imread(img_path)
    h, w = img.shape[:2]

    txt_name = os.path.splitext(file)[0] + ".txt"
    out_path = os.path.join(OUT_DIR, txt_name)

    written = False

    with open(out_path, "w") as out:
        for shape in data.get("shapes", []):
            label = shape.get("label")

            if label not in CLASSES:
                continue

            if shape.get("shape_type") != "polygon":
                continue

            points = shape.get("points", [])
            if len(points) < 3:
                continue

            cls_id = CLASSES.index(label)

            line = [str(cls_id)]
            for x, y in points:
                line.append(f"{x / w:.6f}")
                line.append(f"{y / h:.6f}")

            out.write(" ".join(line) + "\n")
            written = True

    if written:
        count += 1
        print(f"✅ Converted:", file)
    else:
        skipped += 1
        print(f"⚠ No valid labels:", file)

print("\n---------- DONE ----------")
print("Converted :", count)
print("Skipped   :", skipped)
