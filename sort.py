import json
import os
import shutil
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

DATASET = "wjybuqi/traffic-light-detection-dataset"
DATASET_PATH = "train_dataset"
ZIP_FILE = f"{DATASET_PATH}.zip"

data_json = os.path.join(DATASET_PATH, "train.json")
images_root = os.path.join(DATASET_PATH, "train_images")
output_root = os.path.join(DATASET_PATH, "sorted_images")

def download_data():
    if not os.path.exists(DATASET_PATH):
        os.makedirs(DATASET_PATH, exist_ok=True)
        
        api = KaggleApi()
        api.authenticate()
        
        print("Downloading dataset...")
        api.dataset_download_files(DATASET, path=".", unzip=True)
        print("Download complete.")
    else:
        print("Dataset already downloaded.")

download_data()

if not os.path.exists(data_json):
    raise FileNotFoundError(f"JSON file not found: {data_json}")

with open(data_json, "r", encoding="utf-8") as f:
    data = json.load(f)

for annotation in data["annotations"]:
    filename = annotation["filename"]
    file_path = os.path.join(images_root, os.path.basename(filename))

    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist, skipping...")
        continue

    colors = set(inbox["color"] for inbox in annotation.get("inbox", []))

    if not colors:
        continue

    for color in colors:
        color_dir = os.path.join(output_root, color)
        os.makedirs(color_dir, exist_ok=True)
        
        target_path = os.path.join(color_dir, os.path.basename(filename))
        shutil.copy2(file_path, target_path)
        print(f"Copied {file_path} -> {target_path}")

print("Sorting complete!")
