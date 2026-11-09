# Storage Optimization Manual Review Register
**Project:** AgriRoute (spoilage-predictor)  
**Date:** 2026-11-10  
**Guidance:** In accordance with AgriRoute Scientific Integrity Rules, the following high-capacity files and directories were **deliberately retained** during the automated cleanup. They represent important raw artifacts or immutable upstream archives that should only be deleted or moved with explicit human authorization.

---

## 1. Upstream Dataset Source Archives (Immutable Provenance)

The following three ZIP archives contain the original untouched downloads from external repositories. While their contents are extracted in `data/raw/`, keeping the raw ZIP archives ensures cryptographic proof of data provenance and eliminates the need to re-download if extraction integrity is audited:

| Archive Path | Size | SHA-256 Checksum | Actionable Recommendation |
| :--- | :--- | :--- | :--- |
| `data/raw/kaggle/fruits-fresh-and-rotten-for-classification.zip` | 3.58 GB | `8ae77b852ddf6df48c7bd26b0e3255803dbb154d` | **Retain locally** or transfer to institutional cold storage / Google Drive if disk space is critical. |
| `data/raw/sultana/Sultana_Original.zip` | 2.60 GB | `c63afc76940d02664120f98a310a6d2d137b9401` | **Retain locally** or archive off-disk. |
| `data/raw/fruitvision/FruitVision_Original.zip` | 857.19 MB | `b041e0054d9bd4b7b4f7157c250d4798cf50d856` | **Retain locally** or archive off-disk. |

> **Potential Additional Space Savings:** **7.04 GB** if source ZIPs are transferred to external cloud storage.

---

## 2. Git History Object Database (`.git/`)

- **Size:** **19.10 GB**
- **Root Cause:** A historical commit previously tracked raw dataset archives.
- **Safety Rule Enforced:** Under Phase 4 of the repository protocol: *"Do not delete .git. Do not rewrite Git history."*
- **Recommendation:** No destructive git rebase was performed. The active working tree and remote branch `remediation/v4-evidence-consistency` now strictly exclude `data/raw/`. If local disk space becomes critical on this machine, running `git gc --prune=now` after removing stale backup reflogs can reclaim up to 15 GB of local disk space.

---

## 3. Historical Submission Archives

- **`AGRIRoute_REMEDIATION_V3.zip`** (3.71 MB)
  - **Status:** Retained.
  - **Reason:** Documents the exact milestone artifact delivered for external audit verification.

---
*AgriRoute Scientific Integrity and Storage Optimization System.*
