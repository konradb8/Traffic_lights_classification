import json
import os
import shutil
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

# Konfiguracja datasetu Kaggle
DATASET = "wjybuqi/traffic-light-detection-dataset"  # <- Zamień na właściwe ID datasetu
DATASET_PATH = "train_dataset"
ZIP_FILE = f"{DATASET_PATH}.zip"  # Nazwa pliku ZIP

# Ścieżki do plików
data_json = os.path.join(DATASET_PATH, "train.json")
images_root = os.path.join(DATASET_PATH, "train_images")
output_root = os.path.join(DATASET_PATH, "sorted_images")

def download_data():
    """Pobiera i rozpakowuje cały dataset z Kaggle, jeśli jeszcze go nie ma."""
    if not os.path.exists(DATASET_PATH):  # Jeśli folder nie istnieje
        os.makedirs(DATASET_PATH, exist_ok=True)
        
        api = KaggleApi()
        api.authenticate()  # Logowanie do API
        
        print("Pobieranie całego datasetu...")
        api.dataset_download_files(DATASET, path=".", unzip=True)  # Pobiera ZIP i rozpakowuje

        print("Pobieranie zakończone.")
    
    else:
        print("Dataset już pobrany.")

# Pobieranie danych, jeśli są potrzebne
download_data()

# Wczytanie pliku JSON
if not os.path.exists(data_json):
    raise FileNotFoundError(f"Nie znaleziono pliku JSON: {data_json}")

with open(data_json, "r", encoding="utf-8") as f:
    data = json.load(f)

# Sortowanie plików według kolorów
for annotation in data["annotations"]:
    filename = annotation["filename"]
    file_path = os.path.join(images_root, os.path.basename(filename))

    if not os.path.exists(file_path):
        print(f"Plik {file_path} nie istnieje, pomijam...")
        continue

    colors = set(inbox["color"] for inbox in annotation.get("inbox", []))

    if not colors:
        continue

    for color in colors:
        color_dir = os.path.join(output_root, color)
        os.makedirs(color_dir, exist_ok=True)
        
        target_path = os.path.join(color_dir, os.path.basename(filename))
        shutil.copy2(file_path, target_path)
        print(f"Skopiowano {file_path} -> {target_path}")

print("Sortowanie zakończone!")
