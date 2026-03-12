import os
import shutil
from final_image_validator import validate_image, estimate_thresholds

SOURCE = "raw_images"

GOOD = "good_images"
BAD = "bad_images"

os.makedirs(GOOD, exist_ok=True)
os.makedirs(BAD + "/bad_blur", exist_ok=True)
os.makedirs(BAD + "/bad_light", exist_ok=True)
os.makedirs(BAD + "/bad_glare", exist_ok=True)
os.makedirs(BAD + "/bad_crop", exist_ok=True)
os.makedirs(BAD + "/bad_obstruction", exist_ok=True)

image_paths = [
    os.path.join(SOURCE, f)
    for f in os.listdir(SOURCE)
    if f.lower().endswith((".jpg", ".png", ".jpeg"))
]

print("Estimating blur thresholds...")
lap_t, sobel_t = estimate_thresholds(image_paths)

print("Blur thresholds:", lap_t, sobel_t)
print("-" * 50)

for img in os.listdir(SOURCE):
    if img.lower().endswith((".jpg", ".png", ".jpeg")):
        src = os.path.join(SOURCE, img)

        result = validate_image(src, lap_t, sobel_t)

        if result == "good":
            dst = os.path.join(GOOD, img)
        else:
            dst = os.path.join(BAD, result, img)

        shutil.copy(src, dst)
        print(img, "->", result)
