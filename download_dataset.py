#!/usr/bin/env python3
"""
download_dataset.py
===================
Downloads the Kaggle "Fresh and Rotten Fruits" dataset and organises it
into data/images/ with the directory layout expected by the CNN notebook.

Prerequisites
-------------
1. A Kaggle account with an API token saved at ~/.kaggle/kaggle.json
   (or set KAGGLE_USERNAME and KAGGLE_KEY env vars in a .env file).
2. `pip install kaggle` (included in requirements.txt).

Dataset
-------
  kaggle datasets download -d sriramr/fruits-fresh-and-rotten-for-classification
  ~13,000 colour images across 6 classes:
    freshapples, freshbananas, freshoranges,
    rottenapples, rottenbananas, rottenoranges
  We keep only apple, banana; tomato/mango images need a second dataset.

Usage
-----
  python download_dataset.py
"""

import os
import sys
import zipfile
from pathlib import Path

# Optional: load .env for KAGGLE_USERNAME / KAGGLE_KEY
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DATA_DIR   = Path(__file__).parent / "data" / "images"
DATASET_ID = "sriramr/fruits-fresh-and-rotten-for-classification"
ZIP_NAME   = "fruits-fresh-and-rotten-for-classification.zip"


def check_kaggle_credentials() -> None:
    """Verify that Kaggle API credentials are available before downloading."""
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    has_env = os.environ.get("KAGGLE_USERNAME") and os.environ.get("KAGGLE_KEY")
    if not kaggle_json.exists() and not has_env:
        print("❌  Kaggle credentials not found.")
        print("    Option A: place your kaggle.json at ~/.kaggle/kaggle.json")
        print("    Option B: set KAGGLE_USERNAME and KAGGLE_KEY in a .env file")
        sys.exit(1)


def download_and_extract() -> None:
    """Download the dataset ZIP from Kaggle and extract into data/images/."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    zip_path = DATA_DIR / ZIP_NAME
    if zip_path.exists():
        print(f"⏩  ZIP already present at {zip_path} — skipping download.")
    else:
        print(f"⬇️   Downloading dataset: {DATASET_ID}")
        # Import here so the script fails clearly if kaggle isn't installed
        import kaggle  # noqa: F401 — triggers credential init
        os.system(
            f'kaggle datasets download -d "{DATASET_ID}" '
            f'-p "{DATA_DIR}" --unzip'
        )
        print("✅  Download complete.")
        return  # --unzip already extracted; no manual step needed

    # Manual extraction fallback (if --unzip wasn't used)
    print(f"📦  Extracting {zip_path} …")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(DATA_DIR)
    print("✅  Extraction complete.")


def report_structure() -> None:
    """Print a summary of extracted image counts per class."""
    print("\n📂  Extracted image structure:")
    for sub in sorted(DATA_DIR.rglob("*")):
        if sub.is_dir():
            n_images = len(list(sub.glob("*.jpg"))) + len(list(sub.glob("*.png")))
            if n_images > 0:
                rel = sub.relative_to(DATA_DIR)
                print(f"    {rel!s:<40}  {n_images:>5} images")


def main() -> None:
    check_kaggle_credentials()
    download_and_extract()
    report_structure()
    print(
        "\n💡  Next step: open notebooks/01_cnn_training.ipynb "
        "and run all cells."
    )


if __name__ == "__main__":
    main()
