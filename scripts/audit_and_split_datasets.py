#!/usr/bin/env python3
"""
scripts/audit_and_split_datasets.py
===================================
Forensic audit, deduplication, cross-dataset leakage inspection, and
leakage-free stratified partitioning for AgriRoute research revision.

Authors: AgriRoute Research Lab
Date: November 2026
"""

import os
import sys
import re
import glob
import json
import hashlib
import zipfile
import shutil
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set

import numpy as np
import pandas as pd
from PIL import Image
import imagehash
from tqdm import tqdm

SEED = 42
np.random.seed(SEED)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
MANIFEST_DIR = PROJECT_ROOT / "experiments" / "split_manifests"
DATA_CARD_DIR = PROJECT_ROOT / "experiments" / "data_cards"

MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
DATA_CARD_DIR.mkdir(parents=True, exist_ok=True)

CANONICAL_CLASSES = [
    "fresh_apple",
    "fresh_banana",
    "fresh_orange",
    "rotten_apple",
    "rotten_banana",
    "rotten_orange"
]
CLASS_TO_IDX = {cls: idx for idx, cls in enumerate(CANONICAL_CLASSES)}


def extract_base_filename(filename: str) -> str:
    """Extract root image filename before artificial rotations/translations."""
    clean = re.sub(r"^(rotated_by_\d+_|saltandpepper_|translation_)", "", filename)
    return clean.strip()


def compute_md5(filepath: Path) -> str:
    """Compute MD5 hash of a file."""
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def compute_phash(filepath: Path) -> str:
    """Compute perceptual hash (pHash) of an image."""
    try:
        with Image.open(filepath) as img:
            return str(imagehash.phash(img))
    except Exception:
        return ""


def verify_image(filepath: Path) -> Tuple[bool, Tuple[int, int], str, str]:
    """
    Verify image integrity, dimensions, mode, and format.
    Returns: (is_valid, (width, height), mode, error_msg)
    """
    try:
        with Image.open(filepath) as img:
            img.verify()
        with Image.open(filepath) as img:
            width, height = img.size
            mode = img.mode
            return True, (width, height), mode, ""
    except Exception as e:
        return False, (0, 0), "", str(e)


def scan_kaggle_dataset(extracted_dir: Path) -> List[Dict]:
    """Scan and normalize Kaggle dataset files."""
    records = []
    print(f"🔍 Scanning Kaggle dataset at {extracted_dir}...")
    img_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    all_files = [f for f in extracted_dir.glob("**/*.*") if f.suffix.lower() in img_extensions and not f.is_dir()]

    for f in tqdm(all_files, desc="Scanning Kaggle"):
        parent_name = f.parent.name.lower().replace(" ", "").replace("_", "")
        mapped_class = None
        if "freshapple" in parent_name:
            mapped_class = "fresh_apple"
        elif "rottenapple" in parent_name:
            mapped_class = "rotten_apple"
        elif "freshbanana" in parent_name:
            mapped_class = "fresh_banana"
        elif "rottenbanana" in parent_name:
            mapped_class = "rotten_banana"
        elif "freshorange" in parent_name:
            mapped_class = "fresh_orange"
        elif "rottenorange" in parent_name:
            mapped_class = "rotten_orange"

        if mapped_class:
            base_name = extract_base_filename(f.name)
            records.append({
                "filepath": str(f.resolve()),
                "filename": f.name,
                "base_subject_id": f"{mapped_class}_{base_name}",
                "dataset_source": "Kaggle_Sriramr",
                "original_split": "train" if "train" in str(f).lower() else "test",
                "class_name": mapped_class,
                "label_idx": CLASS_TO_IDX[mapped_class]
            })

    print(f"Found {len(records)} candidate images in Kaggle dataset.")
    return records


def scan_fruitvision_dataset(extracted_dir: Path) -> List[Dict]:
    """Scan and normalize FruitVision dataset files for the 6 core classes."""
    records = []
    print(f"🔍 Scanning FruitVision dataset at {extracted_dir}...")
    img_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    all_files = [f for f in extracted_dir.glob("**/*.*") if f.suffix.lower() in img_extensions and not f.is_dir()]

    for f in tqdm(all_files, desc="Scanning FruitVision"):
        path_parts = [p.lower() for p in f.parts]
        
        # Exclude formalin-mixed classes
        if any("formalin" in p for p in path_parts):
            continue

        mapped_class = None
        has_apple = any("apple" in p for p in path_parts)
        has_banana = any("banana" in p for p in path_parts)
        has_orange = any("orange" in p for p in path_parts)
        has_fresh = any("fresh" in p for p in path_parts)
        has_rotten = any("rotten" in p for p in path_parts)

        if has_apple and has_fresh:
            mapped_class = "fresh_apple"
        elif has_apple and has_rotten:
            mapped_class = "rotten_apple"
        elif has_banana and has_fresh:
            mapped_class = "fresh_banana"
        elif has_banana and has_rotten:
            mapped_class = "rotten_banana"
        elif has_orange and has_fresh:
            mapped_class = "fresh_orange"
        elif has_orange and has_rotten:
            mapped_class = "rotten_orange"

        if mapped_class:
            records.append({
                "filepath": str(f.resolve()),
                "filename": f.name,
                "base_subject_id": f"fv_{f.name}",
                "dataset_source": "Mendeley_FruitVision",
                "original_split": "external",
                "class_name": mapped_class,
                "label_idx": CLASS_TO_IDX[mapped_class]
            })

    print(f"Found {len(records)} candidate images in FruitVision matching the 6 canonical classes.")
    return records


def scan_sultana_dataset(extracted_dir: Path) -> List[Dict]:
    """Scan and normalize Sultana et al. Mendeley dataset files."""
    records = []
    print(f"🔍 Scanning Sultana dataset at {extracted_dir}...")
    img_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    all_files = [f for f in extracted_dir.glob("**/*.*") if f.suffix.lower() in img_extensions and not f.is_dir()]

    for f in tqdm(all_files, desc="Scanning Sultana"):
        path_parts = [p.lower() for p in f.parts]
        mapped_class = None

        has_apple = any("apple" in p for p in path_parts)
        has_banana = any("banana" in p for p in path_parts)
        has_orange = any("orange" in p for p in path_parts)
        has_fresh = any("fresh" in p for p in path_parts)
        has_rotten = any("rotten" in p for p in path_parts)

        if has_apple and has_fresh:
            mapped_class = "fresh_apple"
        elif has_apple and has_rotten:
            mapped_class = "rotten_apple"
        elif has_banana and has_fresh:
            mapped_class = "fresh_banana"
        elif has_banana and has_rotten:
            mapped_class = "rotten_banana"
        elif has_orange and has_fresh:
            mapped_class = "fresh_orange"
        elif has_orange and has_rotten:
            mapped_class = "rotten_orange"

        if mapped_class:
            records.append({
                "filepath": str(f.resolve()),
                "filename": f.name,
                "base_subject_id": f"sultana_{f.name}",
                "dataset_source": "Mendeley_Sultana",
                "original_split": "external_sultana",
                "class_name": mapped_class,
                "label_idx": CLASS_TO_IDX[mapped_class]
            })

    print(f"Found {len(records)} candidate images in Sultana dataset matching the 6 canonical classes.")
    return records


def audit_records(records: List[Dict], dataset_label: str) -> Tuple[List[Dict], Dict]:
    """Verify images, compute hashes, detect corrupt/duplicate images."""
    valid_records = []
    corrupt_count = 0
    dimensions = []
    modes = Counter()
    md5_map = defaultdict(list)
    phash_map = defaultdict(list)

    print(f"🔬 Auditing {dataset_label} ({len(records)} files)...")
    for r in tqdm(records, desc=f"Auditing {dataset_label}"):
        fpath = Path(r["filepath"])
        is_valid, (w, h), mode, err = verify_image(fpath)
        if not is_valid:
            corrupt_count += 1
            continue

        md5_val = compute_md5(fpath)
        phash_val = compute_phash(fpath)

        r["width"] = w
        r["height"] = h
        r["mode"] = mode
        r["md5"] = md5_val
        r["phash"] = phash_val

        dimensions.append((w, h))
        modes[mode] += 1
        md5_map[md5_val].append(r["filepath"])
        if phash_val:
            phash_map[phash_val].append(r["filepath"])

        valid_records.append(r)

    widths = [w for w, h in dimensions]
    heights = [h for w, h in dimensions]
    exact_duplicates = sum(len(paths) - 1 for paths in md5_map.values() if len(paths) > 1)
    phash_clusters = sum(len(paths) - 1 for paths in phash_map.values() if len(paths) > 1)

    stats = {
        "dataset": dataset_label,
        "total_scanned": len(records),
        "valid_images": len(valid_records),
        "corrupt_images": corrupt_count,
        "exact_duplicates_md5": exact_duplicates,
        "phash_identical_clusters": phash_clusters,
        "modes": dict(modes),
        "min_width": int(np.min(widths)) if widths else 0,
        "max_width": int(np.max(widths)) if widths else 0,
        "mean_width": float(np.mean(widths)) if widths else 0.0,
        "min_height": int(np.min(heights)) if heights else 0,
        "max_height": int(np.max(heights)) if heights else 0,
        "mean_height": float(np.mean(heights)) if heights else 0.0,
        "class_distribution": dict(Counter(r["class_name"] for r in valid_records))
    }

    return valid_records, stats


def partition_kaggle_group_aware(records: List[Dict]) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Split Kaggle records into 70% Train, 15% Val, 15% Internal Test,
    strictly grouped by base_subject_id (root photo) to prevent artificial
    rotation/translation leakage between partitions!
    """
    print("✂️ Partitioning Kaggle dataset at root photo level (70 / 15 / 15)...")

    # Group by (class_name, base_subject_id)
    class_groups = defaultdict(lambda: defaultdict(list))
    for r in records:
        class_groups[r["class_name"]][r["base_subject_id"]].append(r)

    train_records = []
    val_records = []
    test_records = []

    for cls, groups in class_groups.items():
        subject_keys = list(groups.keys())
        np.random.shuffle(subject_keys)

        total_imgs = sum(len(imgs) for imgs in groups.values())
        target_train = int(total_imgs * 0.70)
        target_val = int(total_imgs * 0.15)

        curr_train = 0
        curr_val = 0

        for sk in subject_keys:
            imgs = groups[sk]
            n_imgs = len(imgs)

            if curr_train + n_imgs <= target_train:
                train_records.extend(imgs)
                curr_train += n_imgs
            elif curr_val + n_imgs <= target_val:
                val_records.extend(imgs)
                curr_val += n_imgs
            else:
                test_records.extend(imgs)

    print(f"Split results: Train={len(train_records)}, Val={len(val_records)}, Test={len(test_records)}")
    return train_records, val_records, test_records


def check_cross_leakage(kaggle_records: List[Dict], external_records: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    """Check for identical MD5 or near-duplicate pHash between Kaggle and External datasets."""
    print("🔍 Auditing cross-dataset leakage...")
    kaggle_md5 = {r["md5"]: r for r in kaggle_records}
    kaggle_phashes = {}
    for r in kaggle_records:
        if r.get("phash"):
            try:
                kaggle_phashes[imagehash.hex_to_hash(r["phash"])] = r
            except Exception:
                pass

    leakage_records = []
    clean_external = []

    for ext_r in tqdm(external_records, desc="Checking external against internal"):
        # MD5 exact match
        if ext_r["md5"] in kaggle_md5:
            matched = kaggle_md5[ext_r["md5"]]
            leakage_records.append({
                "leakage_type": "EXACT_MD5",
                "external_file": ext_r["filepath"],
                "internal_file": matched["filepath"],
                "class_name": ext_r["class_name"]
            })
            continue

        # pHash near match (Hamming <= 2)
        if ext_r.get("phash"):
            try:
                ext_ph = imagehash.hex_to_hash(ext_r["phash"])
                is_near_match = False
                for int_ph, matched in kaggle_phashes.items():
                    if ext_ph - int_ph <= 2:
                        leakage_records.append({
                            "leakage_type": "PHASH_NEAR_DUPLICATE",
                            "external_file": ext_r["filepath"],
                            "internal_file": matched["filepath"],
                            "class_name": ext_r["class_name"]
                        })
                        is_near_match = True
                        break
                if is_near_match:
                    continue
            except Exception:
                pass

        clean_external.append(ext_r)

    print(f"Cross-dataset leakage check: {len(leakage_records)} overlaps detected and pruned.")
    print(f"Clean external test records: {len(clean_external)}")
    return clean_external, leakage_records


def export_manifests(train: List[Dict], val: List[Dict], test_int: List[Dict], test_ext: List[Dict], leaks: List[Dict]):
    """Save partition manifests as CSV files."""
    cols = ["filepath", "filename", "dataset_source", "class_name", "label_idx", "width", "height", "md5", "phash"]

    df_train = pd.DataFrame(train)[cols]
    df_val = pd.DataFrame(val)[cols]
    df_test_int = pd.DataFrame(test_int)[cols]
    df_test_ext = pd.DataFrame(test_ext)[cols] if test_ext else pd.DataFrame(columns=cols)

    df_train.to_csv(MANIFEST_DIR / "train.csv", index=False)
    df_val.to_csv(MANIFEST_DIR / "val.csv", index=False)
    df_test_int.to_csv(MANIFEST_DIR / "test_internal.csv", index=False)
    df_test_ext.to_csv(MANIFEST_DIR / "test_external.csv", index=False)

    if leaks:
        pd.DataFrame(leaks).to_csv(MANIFEST_DIR / "cross_leakage_audit.csv", index=False)

    print(f"✅ Saved manifests to {MANIFEST_DIR}:")
    print(f"   - train.csv: {len(df_train)} rows")
    print(f"   - val.csv: {len(df_val)} rows")
    print(f"   - test_internal.csv: {len(df_test_int)} rows")
    print(f"   - test_external.csv: {len(df_test_ext)} rows")


def main():
    print("🚀 Starting AgriRoute Dataset Audit and Partitioning Protocol...")
    kaggle_dir = RAW_DIR / "kaggle" / "extracted"
    fv_dir = RAW_DIR / "fruitvision" / "extracted"
    sultana_dir = RAW_DIR / "sultana" / "extracted"

    if not kaggle_dir.exists():
        print(f"❌ Kaggle extracted directory {kaggle_dir} not found.")
        return

    kaggle_candidates = scan_kaggle_dataset(kaggle_dir)
    kaggle_valid, kaggle_stats = audit_records(kaggle_candidates, "Kaggle_Sriramr")

    train_records, val_records, test_int_records = partition_kaggle_group_aware(kaggle_valid)

    test_ext_clean = []
    leaks = []
    fv_stats = {}
    if fv_dir.exists():
        fv_candidates = scan_fruitvision_dataset(fv_dir)
        fv_valid, fv_stats = audit_records(fv_candidates, "Mendeley_FruitVision")
        test_ext_clean, leaks = check_cross_leakage(kaggle_valid, fv_valid)

    sultana_stats = {}
    if sultana_dir.exists():
        sultana_candidates = scan_sultana_dataset(sultana_dir)
        sultana_valid, sultana_stats = audit_records(sultana_candidates, "Mendeley_Sultana")

    export_manifests(train_records, val_records, test_int_records, test_ext_clean, leaks)

    audit_summary = {
        "kaggle": kaggle_stats,
        "fruitvision": fv_stats,
        "sultana": sultana_stats,
        "splits": {
            "train_count": len(train_records),
            "val_count": len(val_records),
            "test_internal_count": len(test_int_records),
            "test_external_count": len(test_ext_clean),
            "cross_leakage_pruned": len(leaks)
        }
    }
    with open(PROJECT_ROOT / "experiments" / "metrics" / "dataset_audit_summary.json", "w") as f:
        json.dump(audit_summary, f, indent=2)
    print("✅ Audit and Partitioning Protocol Complete.")


if __name__ == "__main__":
    main()
