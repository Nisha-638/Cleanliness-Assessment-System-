# import pandas as pd
# import os
# import requests
# from tqdm import tqdm
# import random

# # Paths
# csv_path = "C:/Users/Ayushi/dataset/spark_inspection_details_202601270958.csv"
# save_dir = "C:/Users/Ayushi/dataset/dataset/raw_images"

# os.makedirs(save_dir, exist_ok=True)

# # Read CSV
# df = pd.read_csv(csv_path)

# # Choose 1000 random image_ids
# N = min(1000, len(df))
# random_ids = df["image_id"].dropna().sample(n=N, random_state=42)
#   # random_state for reproducibility

# headers = {
#     "User-Agent": "Mozilla/5.0"
# }

# count = 0

# for img_id in tqdm(random_ids):
#     img_id = str(img_id).strip()
    
#     # Construct URL
#     if img_id.endswith(".jpeg"):
#         url = f"https://roams.cris.org.in/imageService/api/s3/getImageDirect/{img_id}"
#     else:
#         url = f"https://roams.cris.org.in/imageService/api/s3/getImageDirect/{img_id}.jpeg"

#     try:
#         r = requests.get(url, headers=headers, timeout=20)

#         if r.status_code == 200 and "image" in r.headers.get("Content-Type",""):
#             with open(f"{save_dir}/img_{count}.jpg", "wb") as f:
#                 f.write(r.content)
#             count += 1
#         else:
#             print("Skipped:", url, r.status_code)

#     except Exception as e:
#         print("Error:", url, e)

# print("Downloaded:", count)

# import pandas as pd
# import os
# import requests
# from tqdm import tqdm

# # Paths
# csv_path = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/spark_inspection_details_202601270958.csv"
# save_dir = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/raw_images"

# os.makedirs(save_dir, exist_ok=True)

# # Read CSV
# df = pd.read_csv(csv_path)

# # Take first 1000 image_ids (not random)
# N = min(1000, len(df))
# image_ids = df["image_id"].dropna().head(N)

# headers = {
#     "User-Agent": "Mozilla/5.0"
# }

# count = 0

# for img_id in tqdm(image_ids):
#     img_id = str(img_id).strip()
    
#     # Construct URL
#     if img_id.endswith(".jpeg"):
#         url = f"https://roams.cris.org.in/imageService/api/s3/getImageDirect/{img_id}"
#     else:
#         url = f"https://roams.cris.org.in/imageService/api/s3/getImageDirect/{img_id}.jpeg"

#     try:
#         r = requests.get(url, headers=headers, timeout=20)

#         if r.status_code == 200 and "image" in r.headers.get("Content-Type",""):
#             with open(f"{save_dir}/img_{count}.jpg", "wb") as f:
#                 f.write(r.content)
#             count += 1
#         else:
#             print("Skipped:", url, r.status_code)

#     except Exception as e:
#         print("Error:", url, e)

# print("Downloaded:", count)
import pandas as pd
import os
import requests
from tqdm import tqdm
import time

csv_path = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/spark_inspection_details_202601270958.csv"
save_dir = "C:/Users/Ayushi/Desktop/sanitation_yolo_project/raw_images"
os.makedirs(save_dir, exist_ok=True)

df = pd.read_csv(csv_path)

TARGET = 1000
image_ids = df["image_id"].dropna().astype(str).unique()

headers = {"User-Agent": "Mozilla/5.0"}

count = 0
failed = []

session = requests.Session()
session.headers.update(headers)

for img_id in tqdm(image_ids):
    if count >= TARGET:
        break

    img_id = img_id.strip()
    if not img_id:
        continue

    success = False

    for ext in ["", ".jpeg", ".jpg", ".png"]:
        name = img_id if img_id.endswith(ext) else img_id + ext
        url = f"https://roams.cris.org.in/imageService/api/s3/getImageDirect/{name}"

        try:
            r = session.get(url, timeout=25)

            if r.status_code == 200 and "image" in r.headers.get("Content-Type", "") and len(r.content) > 5000:
                with open(os.path.join(save_dir, name), "wb") as f:
                    f.write(r.content)
                count += 1
                success = True
                break
        except:
            pass

    if not success:
        failed.append(img_id)

    time.sleep(0.1)

print("\nDownloaded:", count)
print("Failed:", len(failed))

