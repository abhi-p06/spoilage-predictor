#!/usr/bin/env python3
"""
scripts/train_vision_benchmark.py
=================================
Reproducible vision model training pipeline (MobileNetV2, EfficientNetB0, ResNet50)
under strictly controlled experimental conditions for AgriRoute research revision.

Usage:
  python scripts/train_vision_benchmark.py --config experiments/configs/mobilenet_v2.yaml
"""

import os
import sys
import argparse
import random
import yaml
import time
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, callbacks
from tensorflow.keras.applications import mobilenet_v2, efficientnet, resnet50
import mlflow

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def set_seed(seed: int = 42):
    """Enforce strict seed reproducibility across libraries."""
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
    os.environ["TF_DETERMINISTIC_OPS"] = "1"


def get_preprocessor(backbone: str):
    """Return matching preprocessing function for the vision backbone."""
    if backbone == "MobileNetV2":
        return mobilenet_v2.preprocess_input
    elif backbone == "EfficientNetB0":
        return efficientnet.preprocess_input
    elif backbone == "ResNet50":
        return resnet50.preprocess_input
    else:
        raise ValueError(f"Unknown backbone: {backbone}")


def build_tf_dataset(
    manifest_path: Path,
    img_size: Tuple[int, int],
    batch_size: int,
    backbone: str,
    is_training: bool = False,
    augment: bool = False,
    aug_params: Dict = None
) -> tf.data.Dataset:
    """Build high-performance tf.data pipeline from manifest CSV."""
    df = pd.read_csv(manifest_path)
    file_paths = df["filepath"].values
    labels = df["label_idx"].values.astype(np.int32)
    
    preprocess_fn = get_preprocessor(backbone)
    
    # Augmentation layers
    aug_layers = []
    if is_training and augment and aug_params:
        if aug_params.get("horizontal_flip", False):
            aug_layers.append(layers.RandomFlip("horizontal"))
        rot = aug_params.get("rotation_range", 0.0)
        if rot > 0:
            aug_layers.append(layers.RandomRotation(rot))
        zoom = aug_params.get("zoom_range", 0.0)
        if zoom > 0:
            aug_layers.append(layers.RandomZoom((-zoom, zoom)))
        contrast = aug_params.get("contrast_range", 0.0)
        if contrast > 0:
            aug_layers.append(layers.RandomContrast(contrast))
            
    aug_model = tf.keras.Sequential(aug_layers) if aug_layers else None

    def process_image(path_tensor, label_tensor):
        img_bytes = tf.io.read_file(path_tensor)
        img = tf.image.decode_image(img_bytes, channels=3, expand_animations=False)
        img = tf.image.resize(img, img_size)
        img.set_shape([img_size[0], img_size[1], 3])
        if aug_model is not None:
            img = aug_model(img, training=True)
        img = preprocess_fn(img)
        return img, label_tensor

    ds = tf.data.Dataset.from_tensor_slices((file_paths, labels))
    if is_training:
        ds = ds.shuffle(buffer_size=min(len(file_paths), 2000), seed=42, reshuffle_each_iteration=True)
        
    ds = ds.map(process_image, num_parallel_calls=tf.data.AUTOTUNE)
    ds = ds.batch(batch_size)
    ds = ds.prefetch(tf.data.AUTOTUNE)
    return ds, len(df)


def create_model(backbone: str, input_shape: Tuple[int, int, int], num_classes: int) -> Tuple[models.Model, tf.keras.Model]:
    """Instantiate pre-trained backbone with standard classification head."""
    if backbone == "MobileNetV2":
        base_model = mobilenet_v2.MobileNetV2(
            input_shape=input_shape, include_top=False, weights="imagenet", pooling="avg"
        )
    elif backbone == "EfficientNetB0":
        base_model = efficientnet.EfficientNetB0(
            input_shape=input_shape, include_top=False, weights="imagenet", pooling="avg"
        )
    elif backbone == "ResNet50":
        base_model = resnet50.ResNet50(
            input_shape=input_shape, include_top=False, weights="imagenet", pooling="avg"
        )
    else:
        raise ValueError(f"Unsupported backbone: {backbone}")

    inputs = layers.Input(shape=input_shape)
    x = base_model(inputs)
    x = layers.Dropout(0.3, name="top_dropout")(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="predictions", dtype="float32")(x)
    model = models.Model(inputs=inputs, outputs=outputs, name=f"agriroute_{backbone.lower()}")
    return model, base_model


def train_pipeline(config_path: str):
    """Execute training workflow based on configuration YAML."""
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)

    seed = cfg.get("seed", 42)
    set_seed(seed)

    model_name = cfg["model_name"]
    backbone = cfg["backbone"]
    data_cfg = cfg["data"]
    train_cfg = cfg["training"]
    aug_cfg = cfg.get("augmentation", {})
    paths_cfg = cfg["paths"]

    input_res = tuple(data_cfg["input_resolution"][:2])
    input_shape = tuple(data_cfg["input_resolution"])
    batch_size = data_cfg["batch_size"]
    num_classes = data_cfg["num_classes"]

    checkpoint_dir = PROJECT_ROOT / paths_cfg["checkpoint_dir"]
    log_dir = PROJECT_ROOT / paths_cfg["log_dir"]
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    best_model_path = checkpoint_dir / "best_model.keras"
    history_csv_path = log_dir / "training_history.csv"

    print(f"\n========================================================")
    print(f"🚀 Training {model_name} (Backbone: {backbone})")
    print(f"   Input shape: {input_shape}, Batch size: {batch_size}")
    print(f"   Checkpoints: {checkpoint_dir}")
    print(f"========================================================\n")

    # Build datasets
    train_manifest = PROJECT_ROOT / data_cfg["train_manifest"]
    val_manifest = PROJECT_ROOT / data_cfg["val_manifest"]

    train_ds, n_train = build_tf_dataset(
        train_manifest, input_res, batch_size, backbone,
        is_training=True, augment=aug_cfg.get("enabled", True), aug_params=aug_cfg
    )
    val_ds, n_val = build_tf_dataset(
        val_manifest, input_res, batch_size, backbone,
        is_training=False, augment=False
    )

    print(f"Data counts: Train = {n_train} samples, Val = {n_val} samples.")

    # Initialize model
    model, base_model = create_model(backbone, input_shape, num_classes)

    # MLflow Setup
    mlflow.set_tracking_uri(f"sqlite:///{PROJECT_ROOT}/mlflow.db")
    mlflow.set_experiment(cfg.get("experiment_name", "agriroute_vision_benchmark"))

    with mlflow.start_run(run_name=model_name):
        mlflow.log_params({
            "model_name": model_name,
            "backbone": backbone,
            "input_resolution": str(input_shape),
            "batch_size": batch_size,
            "phase1_lr": train_cfg["phase1_lr"],
            "phase1_epochs": train_cfg["phase1_epochs"],
            "phase2_lr": train_cfg["phase2_lr"],
            "phase2_epochs": train_cfg["phase2_epochs"],
            "optimizer": train_cfg["optimizer"],
            "weight_decay": train_cfg["weight_decay"],
            "augmentation_enabled": aug_cfg.get("enabled", True)
        })

        # ---------------------------------------------------------
        # PHASE 1: Feature Extraction (Backbone Frozen)
        # ---------------------------------------------------------
        base_model.trainable = False
        opt_phase1 = optimizers.AdamW(
            learning_rate=train_cfg["phase1_lr"],
            weight_decay=train_cfg["weight_decay"]
        )
        model.compile(
            optimizer=opt_phase1,
            loss=train_cfg["loss"],
            metrics=["accuracy"]
        )

        cb_list = [
            callbacks.ModelCheckpoint(
                filepath=str(best_model_path),
                monitor="val_loss",
                save_best_only=True,
                verbose=1
            ),
            callbacks.EarlyStopping(
                monitor="val_loss",
                patience=train_cfg["early_stopping_patience"],
                restore_best_weights=True,
                verbose=1
            ),
            callbacks.ReduceLROnPlateau(
                monitor="val_loss",
                factor=train_cfg["reduce_lr_factor"],
                patience=train_cfg["reduce_lr_patience"],
                min_lr=train_cfg["min_lr"],
                verbose=1
            ),
            callbacks.CSVLogger(str(history_csv_path), append=False)
        ]

        print(f"\n--- Phase 1: Frozen Backbone Training ({train_cfg['phase1_epochs']} epochs) ---")
        start_time = time.time()
        hist1 = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=train_cfg["phase1_epochs"],
            callbacks=cb_list,
            verbose=1
        )

        # ---------------------------------------------------------
        # PHASE 2: Fine-Tuning (Top Layers Unfrozen)
        # ---------------------------------------------------------
        phase2_epochs = train_cfg.get("phase2_epochs", 0)
        fine_tune_at = train_cfg.get("fine_tune_at", 100)

        if phase2_epochs > 0 and fine_tune_at >= 0:
            print(f"\n--- Phase 2: Fine-Tuning from Layer {fine_tune_at} ({phase2_epochs} epochs) ---")
            base_model.trainable = True
            for layer in base_model.layers[:fine_tune_at]:
                layer.trainable = False

            opt_phase2 = optimizers.AdamW(
                learning_rate=train_cfg["phase2_lr"],
                weight_decay=train_cfg["weight_decay"]
            )
            model.compile(
                optimizer=opt_phase2,
                loss=train_cfg["loss"],
                metrics=["accuracy"]
            )

            # Update logger to append
            cb_list[-1] = callbacks.CSVLogger(str(history_csv_path), append=True)

            hist2 = model.fit(
                train_ds,
                validation_data=val_ds,
                initial_epoch=train_cfg["phase1_epochs"],
                epochs=train_cfg["phase1_epochs"] + phase2_epochs,
                callbacks=cb_list,
                verbose=1
            )

        elapsed = time.time() - start_time
        print(f"✅ Training completed in {elapsed:.2f} seconds.")

        # Evaluate on Validation Set
        best_model = models.load_model(str(best_model_path))
        val_loss, val_acc = best_model.evaluate(val_ds, verbose=0)
        print(f"🏆 Best Model Validation Loss: {val_loss:.4f}, Accuracy: {val_acc:.4f}")

        mlflow.log_metrics({
            "val_loss": val_loss,
            "val_accuracy": val_acc,
            "training_time_seconds": elapsed
        })
        mlflow.log_artifact(str(history_csv_path))
        mlflow.log_artifact(str(best_model_path))

    print(f"✨ Training pipeline for {model_name} finished successfully.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AgriRoute Vision Model Trainer")
    parser.add_argument("--config", type=str, required=True, help="Path to YAML config file")
    args = parser.parse_args()
    train_pipeline(args.config)
