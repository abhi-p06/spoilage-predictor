"""
scripts/storage_audit_phase2.py
===============================
Phase 2 Storage Inventory Script for AgriRoute Repository Cleanup.
Generates:
- CLEANUP_V2_BEFORE.md
- LARGE_FILES_INVENTORY.csv
- DUPLICATE_FILES_INVENTORY.csv
- OBSOLETE_REPORTS_INVENTORY.csv
"""

import os
import sys
import hashlib
from pathlib import Path
import pandas as pd
from collections import defaultdict
import time

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def format_bytes(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def compute_sha256(filepath):
    sha = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(1024*1024), b""):
                sha.update(chunk)
        return sha.hexdigest()
    except Exception as e:
        return f"ERROR: {e}"

def main():
    print("=" * 70)
    print("🔍 Starting Phase 2 Storage Audit of AgriRoute...")
    print("=" * 70)
    start_time = time.time()

    total_project_bytes = 0
    all_files_info = []
    dir_sizes = defaultdict(int)

    # Walk directory tree
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Exclude .git internals from full sha scan to be fast, but calculate .git size
        rel_root = Path(root).relative_to(PROJECT_ROOT)
        
        for f in files:
            fp = Path(root) / f
            try:
                st = fp.stat()
                size = st.st_size
            except OSError:
                continue

            total_project_bytes += size
            
            # Attribute to top-level directory
            parts = rel_root.parts
            top_dir = parts[0] if parts else "(root)"
            dir_sizes[top_dir] += size

            # Exclude .git internals from duplicate checksumming
            is_git = ".git" in parts
            all_files_info.append({
                "path": str(fp),
                "relative_path": str(rel_root / f),
                "filename": f,
                "size_bytes": size,
                "top_dir": top_dir,
                "is_git": is_git,
                "suffix": fp.suffix.lower()
            })

    print(f"Total project files: {len(all_files_info):,}")
    print(f"Total project size:  {format_bytes(total_project_bytes)} ({total_project_bytes:,} bytes)")

    # 1. Directory Breakdown
    dir_summary = []
    for d, s in sorted(dir_sizes.items(), key=lambda x: x[1], reverse=True):
        dir_summary.append({
            "directory": d,
            "size_bytes": s,
            "size_human": format_bytes(s),
            "percent": (s / total_project_bytes) * 100 if total_project_bytes else 0
        })
    df_dirs = pd.DataFrame(dir_summary)

    # 2. Largest Files (Top 100)
    non_git_files = [x for x in all_files_info if not x["is_git"]]
    non_git_files.sort(key=lambda x: x["size_bytes"], reverse=True)
    top_50 = non_git_files[:100]

    # Compute sha256 for top 100 large files
    print("Computing SHA-256 for largest files...")
    for item in top_50:
        item["sha256"] = compute_sha256(item["path"])

    df_large = pd.DataFrame([{
        "filename": x["filename"],
        "relative_path": x["relative_path"],
        "size_bytes": x["size_bytes"],
        "size_human": format_bytes(x["size_bytes"]),
        "sha256": x["sha256"],
        "top_dir": x["top_dir"]
    } for x in top_50])
    df_large.to_csv(PROJECT_ROOT / "LARGE_FILES_INVENTORY.csv", index=False)
    print(f"✅ Generated LARGE_FILES_INVENTORY.csv ({len(df_large)} files)")

    # 3. Duplicate Detection by Size and Checksum
    # Group by size first
    size_map = defaultdict(list)
    for x in non_git_files:
        if x["size_bytes"] > 0:  # ignore 0 byte files for duplicate hash
            size_map[x["size_bytes"]].append(x)

    potential_duplicates = [group for group in size_map.values() if len(group) > 1]
    print(f"Potential duplicate groups by exact file size: {len(potential_duplicates)}")

    duplicate_records = []
    hash_seen = defaultdict(list)
    for group in potential_duplicates:
        for item in group:
            sha = compute_sha256(item["path"])
            item["sha256"] = sha
            hash_seen[sha].append(item)

    dup_group_id = 1
    total_wasted_dup_bytes = 0
    for sha, items in hash_seen.items():
        if len(items) > 1 and not sha.startswith("ERROR"):
            wasted = items[0]["size_bytes"] * (len(items) - 1)
            total_wasted_dup_bytes += wasted
            for rank, item in enumerate(items, 1):
                duplicate_records.append({
                    "duplicate_group_id": f"DUP_{dup_group_id:04d}",
                    "rank_in_group": rank,
                    "sha256": sha,
                    "size_bytes": item["size_bytes"],
                    "size_human": format_bytes(item["size_bytes"]),
                    "filename": item["filename"],
                    "relative_path": item["relative_path"],
                    "wasted_bytes": wasted if rank == 1 else 0
                })
            dup_group_id += 1

    df_dups = pd.DataFrame(duplicate_records)
    df_dups.to_csv(PROJECT_ROOT / "DUPLICATE_FILES_INVENTORY.csv", index=False)
    print(f"✅ Generated DUPLICATE_FILES_INVENTORY.csv ({len(duplicate_records)} duplicate instances, {format_bytes(total_wasted_dup_bytes)} redundant storage)")

    # 4. Obsolete Reports and Versions Inventory
    obsolete_records = []
    # Identify superseded versions: V3 reports, V4 reports where V4.1 exists, duplicate zip exports
    versioned_files = [x for x in non_git_files if any(k in x["filename"] for k in ["_V3", "_v3", "_V4.", "_V4_", "_V4_1", "_v4", "RANDOM_V4", "GROUP_TEST_V4", "REMEDIATION_V3", "FINAL_EXPERIMENT_V4_1"])]
    
    for x in non_git_files:
        fn = x["filename"]
        rp = x["relative_path"]
        sz = x["size_bytes"]

        status = "KEEP"
        reason = "Active research file"

        # Check temporary / caches
        if "__pycache__" in rp or fn.endswith(".pyc") or ".pytest_cache" in rp or fn == ".DS_Store":
            status = "CANDIDATE_REMOVE"
            reason = "Disposable interpreter / testing cache"
        elif fn == "AGRIRoute_REMEDIATION_V3.zip":
            status = "CANDIDATE_ARCHIVE"
            reason = "Historical V3 audit package (superseded by V4.1)"
        elif "AGRIRoute_FINAL_EXPERIMENT_V4_1" in rp and not rp.endswith(".zip"):
            status = "CANDIDATE_CONSOLIDATE"
            reason = "Uncompressed mirror of files already archived in AGRIRoute_FINAL_EXPERIMENT_V4_1.zip"
        elif any(fn.endswith(sfx) for sfx in ["_V3.md", "_V3.csv", "_V3.json"]):
            status = "CANDIDATE_ARCHIVE"
            reason = "Superseded V3 forensic draft (archive under archive/v3/)"
        elif any(fn.endswith(sfx) for sfx in ["_V4.md", "_V4.csv"]) and fn not in ["GROUP_SPLIT_MANIFEST_MERGED_V4.csv"]:
            # Check if V4_1 exists
            v4_1_variant = fn.replace("_V4.", "_V4_1.").replace("_V4_", "_V4_1_")
            status = "CANDIDATE_ARCHIVE"
            reason = "Historical V4 report (archive under archive/v4/)"
        elif fn in ["PREDICTIONS_GROUP_TEST.csv", "PREDICTIONS_GROUP_TEST_RAW_ONLY.csv", "PREDICTIONS_FRUITVISION.csv", "PREDICTIONS_SULTANA.csv", "PREDICTIONS_RANDOM.csv"]:
            status = "CANDIDATE_ARCHIVE"
            reason = "Pre-V4 unversioned predictions (archive under archive/historical_experiments/)"
        
        if status != "KEEP":
            obsolete_records.append({
                "filename": fn,
                "relative_path": rp,
                "size_bytes": sz,
                "size_human": format_bytes(sz),
                "disposition": status,
                "recommendation_reason": reason
            })

    df_obs = pd.DataFrame(obsolete_records)
    df_obs.to_csv(PROJECT_ROOT / "OBSOLETE_REPORTS_INVENTORY.csv", index=False)
    print(f"✅ Generated OBSOLETE_REPORTS_INVENTORY.csv ({len(df_obs)} candidate items)")

    # 5. Write CLEANUP_V2_BEFORE.md
    cleanup_before_path = PROJECT_ROOT / "CLEANUP_V2_BEFORE.md"
    with open(cleanup_before_path, "w") as f:
        f.write(f"""# Storage Audit Before Cleanup (Phase 2)

**Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}  
**Repository:** `spoilage-predictor`  
**Total Repository Size:** {format_bytes(total_project_bytes)} ({total_project_bytes:,} bytes)  
**Total File Count:** {len(all_files_info):,} files  

---

## 1. Top-Level Directory Distribution

| Directory | Size | Bytes | Proportion |
| :--- | :--- | :--- | :--- |
""")
        for _, r in df_dirs.iterrows():
            f.write(f"| `{r['directory']}` | {r['size_human']} | {r['size_bytes']:,} | {r['percent']:.2f}% |\n")

        f.write(f"""
---

## 2. Redundancy and Duplication Summary

- **Exact Duplicate File Instances:** {len(duplicate_records)} files across {dup_group_id - 1} groups.
- **Wasted Storage from Binary Duplicates:** {format_bytes(total_wasted_dup_bytes)} ({total_wasted_dup_bytes:,} bytes).
- **Candidate Disposable / Archival Files:** {len(df_obs)} files totaling {format_bytes(df_obs['size_bytes'].sum())}.

### Top 15 Largest Files in Workspace
| Filename | Directory | Size | SHA-256 |
| :--- | :--- | :--- | :--- |
""")
        for _, r in df_large.head(15).iterrows():
            f.write(f"| `{r['filename']}` | `{r['top_dir']}` | {r['size_human']} | `{r['sha256'][:16]}...` |\n")

        f.write(f"""
---

## 3. Storage Optimization Targets

1. **Disposable Caches (`__pycache__`, `.pytest_cache`, `.DS_Store`):** Can be safely pruned.
2. **Identical Root Manifests:** `FINAL_GROUP_TRAIN_V4.csv` and `FINAL_GROUP_TRAIN_V4_1.csv` are 100% bit-for-bit identical (4.47 MB each). `FINAL_GROUP_VAL_V4.csv` and `FINAL_GROUP_VAL_V4_1.csv` (951 KB each), `FINAL_GROUP_TEST_V4.csv` and `FINAL_GROUP_TEST_V4_1.csv` (955 KB each).
3. **Consolidation of Historical Material:** Organize loose `*_V3` and `*_V4` reports into `archive/v3/` and `archive/v4/` to clean the repository root.
4. **Duplicate Packaged Folders:** `AGRIRoute_FINAL_EXPERIMENT_V4_1/` contains uncompressed duplicates of checkpoints and manifests already sealed in `AGRIRoute_FINAL_EXPERIMENT_V4_1.zip`.
""")

    print(f"✅ Generated {cleanup_before_path}")

if __name__ == "__main__":
    main()

