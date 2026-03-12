import pandas as pd
import os
import requests
from tqdm import tqdm
import time
import random

# ---------------- FILE PATHS ----------------
rating_csv = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/spark_inspection_rating_202602111506.csv"
details_csv = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/spark_inspection_details_202602111506.csv"

save_base = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/rating_image"
os.makedirs(save_base, exist_ok=True)

# ---------------- LOAD CSV ----------------
rating_df = pd.read_csv(rating_csv, low_memory=False)
details_df = pd.read_csv(details_csv, low_memory=False)

# ---------------- CLEAN TEXT ----------------
rating_df["rating_value"] = rating_df["rating_value"].astype(str).str.lower().str.strip()
rating_df["rating_value_ai"] = rating_df["rating_value_ai"].astype(str).str.lower().str.strip()

# ---------------- JOIN USING inspection_id ----------------
merged_df = pd.merge(
    rating_df,
    details_df,
    on="inspection_id",
    how="inner"
)

print("Total merged rows:", len(merged_df))

# ---------------- FILTER COMMON AGREEMENT ----------------
bad_df = merged_df[
    (merged_df["rating_value"] == "poor") &
    (merged_df["rating_value_ai"] == "bad")
]

avg_df = merged_df[
    (merged_df["rating_value"] == "average") &
    (merged_df["rating_value_ai"] == "medium")
]

good_df = merged_df[
    (merged_df["rating_value"] == "good") &
    (merged_df["rating_value_ai"] == "good")
]

print("Available BAD:", len(bad_df))
print("Available AVERAGE:", len(avg_df))
print("Available GOOD:", len(good_df))


# ---------------- DOWNLOAD FUNCTION ----------------
def download_category(df, folder_name, target_limit=1000):

    save_dir = os.path.join(save_base, folder_name)
    os.makedirs(save_dir, exist_ok=True)

    image_ids = df["image_id"].dropna().astype(str).unique()
    image_ids = list(image_ids)

    random.shuffle(image_ids)

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    count = 0
    attempted = 0

    for img_name in tqdm(image_ids, desc=f"Downloading {folder_name}"):

        if count >= target_limit:
            break

        img_name = img_name.strip()
        url = f"https://roams.cris.org.in/imageService/api/s3/getImageDirect/{img_name}"

        attempted += 1

        try:
            r = session.get(url, timeout=25)

            if (
                r.status_code == 200
                and "image" in r.headers.get("Content-Type", "")
                and len(r.content) > 5000
            ):
                file_path = os.path.join(save_dir, img_name)

                # Avoid overwriting if already exists
                if not os.path.exists(file_path):
                    with open(file_path, "wb") as f:
                        f.write(r.content)

                    count += 1

        except:
            pass

        time.sleep(0.05)

    print(f"\n✅ {folder_name} successfully downloaded: {count}")
    print(f"📦 Total attempted: {attempted}\n")


# ---------------- DOWNLOAD 1000 EACH ----------------
download_category(bad_df, "bad_images", 1000)
download_category(avg_df, "average_images", 1000)
download_category(good_df, "good_images", 1000)

print("🎉 DONE — Download process completed.")
