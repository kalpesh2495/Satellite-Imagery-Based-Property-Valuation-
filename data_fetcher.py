"""
datafetcher.py

Demonstration of satellite imagery data fetching using ESRI World Imagery.
The pipeline fetches a small sample (10 images) for demonstration purposes.
The same code can be scaled to the full dataset by disabling demo mode.
"""

import os
import time
import requests
import pandas as pd
from tqdm import tqdm
from PIL import Image
from io import BytesIO

# =========================
# CONFIG
# =========================
IMAGE_DIR = "data_final/images_final"
os.makedirs(IMAGE_DIR, exist_ok=True)

IMG_SIZE = 224
ZOOM_DELTA = 0.002          # smaller value = more zoomed-in
REQUEST_SLEEP = 0.2        # rate limiting (important for public APIs)

# =========================
# IMAGE FETCH FUNCTION
# =========================
def fetch_esri_image(lat: float, lon: float) -> Image.Image:
    """
    Fetch satellite image from ESRI World Imagery for given latitude & longitude.
    """
    bbox = f"{lon - ZOOM_DELTA},{lat - ZOOM_DELTA},{lon + ZOOM_DELTA},{lat + ZOOM_DELTA}"

    url = (
        "https://services.arcgisonline.com/ArcGIS/rest/services/"
        "World_Imagery/MapServer/export"
    )

    params = {
        "bbox": bbox,
        "bboxSR": 4326,
        "imageSR": 4326,
        "size": f"{IMG_SIZE},{IMG_SIZE}",
        "format": "png",
        "dpi": 96,
        "f": "image"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    return Image.open(BytesIO(response.content))


# =========================
# MAIN FETCH PIPELINE
# =========================
def fetch_images(df: pd.DataFrame):
    """
    Fetch and save satellite images for rows in dataframe.
    Expected columns: ['lat', 'long']
    """
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        img_path = os.path.join(IMAGE_DIR, f"{idx}.png")

        if os.path.exists(img_path):
            continue

        try:
            img = fetch_esri_image(row["lat"], row["long"])
            img.save(img_path)

            # Rate limiting to respect ESRI API
            time.sleep(REQUEST_SLEEP)

        except Exception as e:
            print(f"[ERROR] Failed at index {idx}: {e}")


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    # Load metadata (update path if needed)
    df = pd.read_excel('train(1).xlsx')

    # DEMO MODE (safe for reviewers)
    DEMO_MODE = True   # set to False for full dataset run

    if DEMO_MODE:
        print("Running in DEMO mode: fetching 10 images only")
        df_run = df.head(10)
    else:
        print("Running FULL mode: fetching all images")
        df_run = df

    fetch_images(df_run)

