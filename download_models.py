import os
import gdown
import zipfile
from pathlib import Path

# Названия моделей и их Google Drive-ссылки (или ID в виде `uc?id=...`)
MODELS = {
    "RoBERTa": "https://drive.google.com/uc?id=1pnedZs2l_nXaiZ3M6yFIwovv5pLY6WpY",
    "SecRoBERTa": "https://drive.google.com/uc?id=19B5NLbjB6ZEdtOAFoslEK_rK0z7FcOWS"
}

MODELS_DIR = Path(__file__).parent / "models"
MODELS_DIR.mkdir(exist_ok=True)

def download_and_extract(name: str, url: str):
    target_dir = MODELS_DIR / name
    zip_path = MODELS_DIR / f"{name}.zip"

    if target_dir.exists():
        print(f"[✓] Модель '{name}' уже загружена.")
        return

    print(f"[↓] Загружаем модель '{name}'...")
    gdown.download(url, str(zip_path), quiet=False)

    print(f"[⇩] Распаковываем в {target_dir}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(MODELS_DIR)

    zip_path.unlink()
    print(f"[✓] Готово: {name}\n")

def ensure_models():
    for name, url in MODELS.items():
        download_and_extract(name, url)

if __name__ == "__main__":
    ensure_models()