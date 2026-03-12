import cv2
import numpy as np
import os

# ---------------- BLUR METRICS ----------------
def blur_metrics(gray):
    lap = cv2.Laplacian(gray, cv2.CV_64F).var()
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel = np.mean(np.sqrt(sobelx**2 + sobely**2))
    return lap, sobel


# ---------------- THRESHOLD ESTIMATION ----------------
def estimate_thresholds(image_paths):
    laps, sobels = [], []

    for p in image_paths[:40]:
        img = cv2.imread(p)
        if img is None:
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        lap, sobel = blur_metrics(gray)
        laps.append(lap)
        sobels.append(sobel)

    lap_thresh = np.mean(laps) - 0.5 * np.std(laps)
    sobel_thresh = np.mean(sobels) - 0.5 * np.std(sobels)

    return lap_thresh, sobel_thresh


# ---------------- MAIN VALIDATOR ----------------
def validate_image(path, blur_thresh_lap, blur_thresh_sobel):
    img = cv2.imread(path)

    if img is None:
        return "bad_obstruction"

    h, w = img.shape[:2]
    if h < 150 or w < 150:
        return "bad_crop"

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    lap, sobel = blur_metrics(gray)
    mean_light = np.mean(gray)
    glare_ratio = np.sum(gray > 240) / gray.size

    print(f"{os.path.basename(path)} | lap={lap:.1f} sobel={sobel:.1f} light={mean_light:.1f} glare={glare_ratio:.3f}")

    # ---- ORDER IMPROVED ----
    if mean_light < 40 or mean_light > 215:
        return "bad_light"

    if glare_ratio > 0.12:
        return "bad_glare"

    if lap < blur_thresh_lap and sobel < blur_thresh_sobel:
        return "bad_blur"

    return "good"
