# import os
# import random
# import shutil

# # ---------------- CONFIG ----------------
# BASE_DIR = os.getcwd()

# IMG_DIR = os.path.join(BASE_DIR, "good_images")
# LABEL_DIR = os.path.join(BASE_DIR, "yolo_dataset", "labels", "train")

# OUT_IMG_TRAIN = os.path.join(BASE_DIR, "yolo_dataset", "images", "train")
# OUT_IMG_VAL   = os.path.join(BASE_DIR, "yolo_dataset", "images", "val")

# OUT_LAB_TRAIN = os.path.join(BASE_DIR, "yolo_dataset", "labels", "train_split")
# OUT_LAB_VAL   = os.path.join(BASE_DIR, "yolo_dataset", "labels", "val")

# SPLIT_RATIO = 0.8

# # ---------------- CREATE FOLDERS ----------------
# os.makedirs(OUT_IMG_TRAIN, exist_ok=True)
# os.makedirs(OUT_IMG_VAL, exist_ok=True)
# os.makedirs(OUT_LAB_TRAIN, exist_ok=True)
# os.makedirs(OUT_LAB_VAL, exist_ok=True)

# # ---------------- LOAD FILES ----------------
# images = [f for f in os.listdir(IMG_DIR)
#           if f.lower().endswith((".jpg", ".jpeg", ".png"))]

# random.shuffle(images)

# split_index = int(len(images) * SPLIT_RATIO)

# train_imgs = images[:split_index]
# val_imgs   = images[split_index:]

# print(f"📊 Total images: {len(images)}")
# print(f"📂 Train: {len(train_imgs)}")
# print(f"📁 Val: {len(val_imgs)}")

# # ---------------- MOVE ----------------
# def move_files(img_list, out_img_dir, out_lab_dir):
#     for img in img_list:
#         name = os.path.splitext(img)[0]

#         src_img = os.path.join(IMG_DIR, img)
#         src_lab = os.path.join(LABEL_DIR, name + ".txt")

#         if not os.path.exists(src_lab):
#             print("⚠ Missing label:", img)
#             continue

#         shutil.copy(src_img, os.path.join(out_img_dir, img))
#         shutil.copy(src_lab, os.path.join(out_lab_dir, name + ".txt"))

# move_files(train_imgs, OUT_IMG_TRAIN, OUT_LAB_TRAIN)
# move_files(val_imgs, OUT_IMG_VAL, OUT_LAB_VAL)

# print("\n✅ Dataset split completed!")
# import os
# import random
# import shutil

# # ---------------- CONFIG ----------------
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# IMG_SRC   = os.path.join(BASE_DIR, "raw_images")
# LABEL_SRC = os.path.join(BASE_DIR, "yolo_dataset", "labels", "all")

# IMG_TRAIN = os.path.join(BASE_DIR, "yolo_dataset", "images", "train")
# IMG_VAL   = os.path.join(BASE_DIR, "yolo_dataset", "images", "val")

# LAB_TRAIN = os.path.join(BASE_DIR, "yolo_dataset", "labels", "train")
# LAB_VAL   = os.path.join(BASE_DIR, "yolo_dataset", "labels", "val")

# SPLIT_RATIO = 0.8

# # ---------------- SETUP ----------------
# os.makedirs(IMG_TRAIN, exist_ok=True)
# os.makedirs(IMG_VAL, exist_ok=True)
# os.makedirs(LAB_TRAIN, exist_ok=True)
# os.makedirs(LAB_VAL, exist_ok=True)

# # ---------------- LOAD FILES ----------------
# images = [f for f in os.listdir(IMG_SRC) if f.lower().endswith((".jpg", ".png", ".jpeg"))]

# random.shuffle(images)

# split_idx = int(len(images) * SPLIT_RATIO)
# train_imgs = images[:split_idx]
# val_imgs   = images[split_idx:]

# print(f"Total images : {len(images)}")
# print(f"Train images : {len(train_imgs)}")
# print(f"Val images   : {len(val_imgs)}")

# # ---------------- SPLIT ----------------
# def copy_pair(img_name, img_dst, lab_dst):
#     shutil.copy(os.path.join(IMG_SRC, img_name), os.path.join(img_dst, img_name))

#     label_name = os.path.splitext(img_name)[0] + ".txt"
#     label_path = os.path.join(LABEL_SRC, label_name)

#     if os.path.exists(label_path):
#         shutil.copy(label_path, os.path.join(lab_dst, label_name))
#     else:
#         print("⚠ Missing label:", label_name)

# for img in train_imgs:
#     copy_pair(img, IMG_TRAIN, LAB_TRAIN)

# for img in val_imgs:
#     copy_pair(img, IMG_VAL, LAB_VAL)

# print("\n✅ Dataset split complete.")
import os
import random
import shutil

# ---------------- CONFIG ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMG_SRC   = os.path.join(BASE_DIR, "raw_images")
LABEL_SRC = os.path.join(BASE_DIR, "yolo_dataset", "labels", "all")

IMG_TRAIN = os.path.join(BASE_DIR, "yolo_dataset", "images", "train")
IMG_VAL   = os.path.join(BASE_DIR, "yolo_dataset", "images", "val")

LAB_TRAIN = os.path.join(BASE_DIR, "yolo_dataset", "labels", "train")
LAB_VAL   = os.path.join(BASE_DIR, "yolo_dataset", "labels", "val")

SPLIT_RATIO = 0.8

# ---------------- SETUP ----------------
os.makedirs(IMG_TRAIN, exist_ok=True)
os.makedirs(IMG_VAL, exist_ok=True)
os.makedirs(LAB_TRAIN, exist_ok=True)
os.makedirs(LAB_VAL, exist_ok=True)

# ---------------- LOAD ONLY LABELED FILES ----------------
label_files = [f for f in os.listdir(LABEL_SRC) if f.endswith(".txt")]

images = []
for lab in label_files:
    base = os.path.splitext(lab)[0]

    for ext in [".jpg", ".jpeg", ".png"]:
        img_path = os.path.join(IMG_SRC, base + ext)
        if os.path.exists(img_path):
            images.append(base + ext)
            break

random.shuffle(images)

split_idx = int(len(images) * SPLIT_RATIO)
train_imgs = images[:split_idx]
val_imgs   = images[split_idx:]

print(f"Total labeled images : {len(images)}")
print(f"Train images        : {len(train_imgs)}")
print(f"Val images          : {len(val_imgs)}")

# ---------------- SPLIT ----------------
def copy_pair(img_name, img_dst, lab_dst):
    shutil.copy(os.path.join(IMG_SRC, img_name), os.path.join(img_dst, img_name))

    label_name = os.path.splitext(img_name)[0] + ".txt"
    shutil.copy(os.path.join(LABEL_SRC, label_name), os.path.join(lab_dst, label_name))

for img in train_imgs:
    copy_pair(img, IMG_TRAIN, LAB_TRAIN)

for img in val_imgs:
    copy_pair(img, IMG_VAL, LAB_VAL)

print("\n✅ Dataset split complete (only labeled images used).")
