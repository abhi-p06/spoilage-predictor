# Model B (V4.1) Primary Training Report: Raw-Only ImageNet Fine-Tuning

**Model Identifier:** `agriroute_mobilenet_v2_v4_1_primary`  
**Checkpoint Path:** `experiments/group_leakage_study/CHECKPOINTS/group_aware_mobilenet_v2_v4_1.keras`  
**Root Alias:** `MODEL_B_V4_1_CHECKPOINT.keras`  
**SHA-256 Checksum:** `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4`  
**Training Date:** 2026-11-09 20:31:32 UTC  
**Total Training Duration:** 155.6 seconds (2.59 minutes)  

---

## 1. Experimental Design & Partition Rigor

- **Primary Experiment Mandate:** Trained strictly on original fruit specimen screenshots identified by `is_raw == 1`.
- **Training Partition:** Exactly 1,057 raw screenshots from `FINAL_GROUP_TRAIN_V4_1.csv`.
- **Validation Partition:** Exactly 227 unaugmented raw screenshots from `FINAL_GROUP_VAL_V4_1.csv` (used solely for early stopping and temperature scaling).
- **Test Partition:** Exactly 227 unaugmented raw screenshots from `FINAL_GROUP_TEST_V4_1.csv` (completely unobserved during training and tuning).
- **Online Augmentation:** Applied during runtime strictly to the 1,057 training images (RandomFlip, RandomRotation(0.15), RandomZoom(0.10), RandomContrast(0.10)). Validation and test remain unaugmented.

---

## 2. Hyperparameter Configuration

| Hyperparameter | Phase 1 (Feature Extraction) | Phase 2 (Fine-Tuning) |
| :--- | :--- | :--- |
| **Backbone Trainability** | Frozen (`trainable=False`) | Layers 100–154 Trainable (Layers 0–99 Frozen) |
| **Optimizer** | AdamW (`weight_decay=1e-4`) | AdamW (`weight_decay=1e-4`) |
| **Learning Rate** | $1.0 \times 10^-3$ | $1.0 \times 10^-4$ (with `ReduceLROnPlateau(factor=0.2, patience=3)`) |
| **Loss Function** | Categorical Crossentropy (`label_smoothing=0.05`) | Categorical Crossentropy (`label_smoothing=0.05`) |
| **Batch Size** | 32 | 32 |
| **Epochs Scheduled** | 10 | 20 (epochs 11 to 30) |
| **Early Stopping** | Patience = 5 on `val_loss` | Patience = 5 on `val_loss` |
| **Input Preprocessing** | `mobilenet_v2.preprocess_input` ($[-1, 1]$) | `mobilenet_v2.preprocess_input` ($[-1, 1]$) |
| **Random Seed** | 42 | 42 |

---

## 3. Training Trajectory & Convergence

- **Best Validation Epoch:** Epoch 10
- **Best Validation Loss:** 0.3526
- **Validation Accuracy at Best Epoch:** 96.92%
- **Training Accuracy at Best Epoch:** 98.30%

### Complete Epoch History
```csv
epoch,accuracy,learning_rate,loss,val_accuracy,val_loss
0,0.6234626173973083,0.0010000000474974,1.1308565139770508,0.933920681476593,0.5005279183387756
1,0.8968779444694519,0.0010000000474974,0.5160296559333801,0.9603524208068848,0.4046975672245025
2,0.9290444850921632,0.0010000000474974,0.4508436620235443,0.9603524208068848,0.3800356388092041
3,0.9460737705230712,0.0010000000474974,0.4167973399162292,0.9647576808929444,0.3786774277687073
4,0.9621570706367492,0.0010000000474974,0.3872841596603393,0.9647576808929444,0.366078108549118
5,0.964049220085144,0.0010000000474974,0.3851127028465271,0.9603524208068848,0.3619720935821533
6,0.9735099077224731,0.0010000000474974,0.368895560503006,0.9647576808929444,0.3606068193912506
7,0.9744560122489928,0.0010000000474974,0.3645370900630951,0.9691630005836488,0.3548215925693512
8,0.9801324605941772,0.0010000000474974,0.3647317886352539,0.9691630005836488,0.3555740118026733
9,0.982970654964447,0.0010000000474974,0.3501348197460174,0.9691630005836488,0.3525950014591217
10,0.9157994389533995,9.999999747378752e-05,0.4965964555740356,0.7665198445320129,0.938836634159088
11,0.9659413695335388,9.999999747378752e-05,0.3778336346149444,0.7709251046180725,0.9101333022117616
12,0.975402057170868,9.999999747378752e-05,0.356392353773117,0.7797356843948364,0.933996856212616
13,0.975402057170868,1.9999999494757503e-05,0.3533191084861755,0.8017621040344238,0.8399487733840942
14,0.990539252758026,1.9999999494757503e-05,0.3258782625198364,0.8193832635879517,0.7625094056129456

```

---

## 4. Software Environment Manifest
- **Platform:** macOS Darwin (Apple Silicon M4, Metal GPU PluggableDevice)
- **TensorFlow Version:** 2.16.2
- **NumPy Version:** 1.26.4
- **Pandas Version:** 2.2.3
