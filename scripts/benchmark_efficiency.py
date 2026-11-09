#!/usr/bin/env python3
"""
scripts/benchmark_efficiency.py
===============================
Measures edge deployment efficiency for AgriRoute vision models:
- Parameter count (total, trainable, non-trainable)
- Model checkpoint file size on disk (MB)
- Inference latency (CPU and Metal/GPU) at batch size 1 and 32 (warm-up + 100 runs)
- Peak memory usage (RSS and tracemalloc)

Usage:
  python scripts/benchmark_efficiency.py
"""

import os
import sys
import time
import json
import tracemalloc
import resource
from pathlib import Path
from typing import Dict, List

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def get_model_file_size_mb(filepath: Path) -> float:
    """Return model file size on disk in megabytes."""
    return filepath.stat().st_size / (1024 * 1024)


def count_parameters(model: tf.keras.Model) -> Dict[str, int]:
    """Count total, trainable, and non-trainable parameters."""
    total_params = model.count_params()
    trainable_params = sum(np.prod(p.shape) for p in model.trainable_weights)
    non_trainable_params = total_params - trainable_params
    return {
        "total_params": int(total_params),
        "trainable_params": int(trainable_params),
        "non_trainable_params": int(non_trainable_params)
    }


def measure_latency(model: tf.keras.Model, input_shape: tuple, batch_size: int, n_runs: int = 100) -> Dict[str, float]:
    """Measure inference latency in milliseconds over n_runs after 10 warm-up runs."""
    dummy_input = tf.random.normal((batch_size, *input_shape))

    # Warm-up
    for _ in range(10):
        _ = model(dummy_input, training=False)

    latencies = []
    for _ in range(n_runs):
        start = time.perf_counter()
        _ = model(dummy_input, training=False)
        latencies.append((time.perf_counter() - start) * 1000.0)  # ms

    latencies = np.array(latencies)
    return {
        "mean_ms": float(np.mean(latencies)),
        "std_ms": float(np.std(latencies)),
        "median_ms": float(np.median(latencies)),
        "p95_ms": float(np.percentile(latencies, 95)),
        "min_ms": float(np.min(latencies)),
        "max_ms": float(np.max(latencies)),
        "per_sample_ms": float(np.mean(latencies) / batch_size),
        "throughput_fps": float((batch_size * 1000.0) / np.mean(latencies))
    }


def benchmark_model(model_dir_name: str, backbone: str, input_res: tuple) -> Dict:
    """Run full efficiency profile for a trained model or instantiated architecture."""
    ckpt_path = PROJECT_ROOT / "experiments" / "checkpoints" / model_dir_name / "best_model.keras"
    file_size_mb = 0.0

    print(f"\n⚡ Benchmarking {model_dir_name} ({backbone})...")
    # Start memory profiling
    tracemalloc.start()
    start_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    if ckpt_path.exists():
        file_size_mb = get_model_file_size_mb(ckpt_path)
        model = load_model(str(ckpt_path))
    else:
        # Instantiate architecture directly
        from train_vision_benchmark import create_model
        model, _ = create_model(backbone, input_res, 6)
        # Approximate file size (parameters * 4 bytes / 1024 / 1024)
        file_size_mb = (model.count_params() * 4) / (1024 * 1024)

    param_counts = count_parameters(model)

    # Measure latency at batch size 1 (edge single-shot)
    lat_b1 = measure_latency(model, input_res, batch_size=1, n_runs=100)

    # Measure latency at batch size 32 (throughput batch)
    lat_b32 = measure_latency(model, input_res, batch_size=32, n_runs=50)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    # On macOS, ru_maxrss is in bytes; on Linux in kilobytes
    rss_mb = (end_rss - start_rss) / (1024 * 1024) if sys.platform == "darwin" else (end_rss - start_rss) / 1024

    profile = {
        "model_name": model_dir_name,
        "backbone": backbone,
        "input_resolution": list(input_res),
        "file_size_mb": float(file_size_mb),
        "parameters": param_counts,
        "latency_batch_1": lat_b1,
        "latency_batch_32": lat_b32,
        "peak_tracemalloc_mb": float(peak / (1024 * 1024)),
        "delta_rss_mb": float(rss_mb)
    }

    print(f"   Size: {file_size_mb:.2f} MB | Total Params: {param_counts['total_params']:,}")
    print(f"   Latency (B=1): {lat_b1['mean_ms']:.2f} ± {lat_b1['std_ms']:.2f} ms ({lat_b1['throughput_fps']:.1f} FPS)")
    print(f"   Latency (B=32): {lat_b32['mean_ms']:.2f} ms ({lat_b32['throughput_fps']:.1f} FPS)")
    return profile


def main():
    print("🚀 Running Deployment Efficiency Benchmarking Protocol...")
    models_to_bench = [
        ("mobilenet_v2", "MobileNetV2", (224, 224, 3)),
        ("efficientnet_b0", "EfficientNetB0", (224, 224, 3)),
        ("resnet50", "ResNet50", (224, 224, 3)),
        ("ablation_frozen", "MobileNetV2", (224, 224, 3)),
        ("ablation_res160", "MobileNetV2", (160, 160, 3)),
        ("ablation_no_aug", "MobileNetV2", (224, 224, 3))
    ]

    all_profiles = []
    for model_name, backbone, input_res in models_to_bench:
        prof = benchmark_model(model_name, backbone, input_res)
        if prof:
            all_profiles.append(prof)

    out_path = PROJECT_ROOT / "experiments" / "metrics" / "deployment_efficiency.json"
    with open(out_path, "w") as f:
        json.dump(all_profiles, f, indent=2)

    print(f"\n✅ Deployment efficiency profiles saved to {out_path}")


if __name__ == "__main__":
    main()

