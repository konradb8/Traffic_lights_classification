import json
import os
import shutil
from kaggle.api.kaggle_api_extended import KaggleApi

# Kaggle dataset configuration
DATASET = "wjybuqi/traffic-light-detection-dataset"  # <- Replace with the correct dataset ID
DATASET_PATH = "train_dataset"
ZIP_FILE = f"{DATASET_PATH}.zip"  # ZIP file name

# File paths
data_json = os.path.join(DATASET_PATH, "train.json")
images_root = os.path.join(DATASET_PATH, "train_images")
output_root = os.path.join(DATASET_PATH, "train_images")

def download_data():
    """Downloads and extracts the entire dataset from Kaggle if it is not already present."""
    if not os.path.exists(DATASET_PATH):  # If the folder does not exist
        os.makedirs(DATASET_PATH, exist_ok=True)
        
        api = KaggleApi()
        api.authenticate()  # Authenticate API
        
        print("Downloading the entire dataset...")
        api.dataset_download_files(DATASET, path=".", unzip=True)  # Download ZIP and extract

        print("Download completed.")
    
    else:
        print("Dataset already downloaded.")

# Download data if needed
download_data()

# Load JSON file
if not os.path.exists(data_json):
    raise FileNotFoundError(f"JSON file not found: {data_json}")

with open(data_json, "r", encoding="utf-8") as f:
    data = json.load(f)

# Check if dataset is already sorted
if any(os.path.isdir(os.path.join(output_root, d)) for d in os.listdir(output_root)):
    print("Dataset already sorted.")
else:
    # Store sorted files
    sorted_files = set()
    unclassified_root = os.path.join(output_root, "no_traffic_light")  # Place unclassified folder inside sorted images
    os.makedirs(unclassified_root, exist_ok=True)

    # Sort files by color
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
            sorted_files.add(file_path)
            print(f"Copied {file_path} -> {target_path}")

        # Remove file after moving
        os.remove(file_path)
        print(f"Deleted {file_path}")

    # Move files that were not sorted to unclassified folder
    for file in os.listdir(images_root):
        file_path = os.path.join(images_root, file)
        if os.path.isfile(file_path) and file_path not in sorted_files:
            target_path = os.path.join(unclassified_root, file)
            shutil.move(file_path, target_path)
            print(f"Moved uncategorized file to {target_path}")

    print("Sorting completed!")
