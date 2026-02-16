#!/usr/bin/env python3
"""
MLX LoRA Fine-Tuning Pipeline for AECai

End-to-end orchestration: split data, train LoRA adapter, fuse weights,
convert to GGUF, and register with Ollama.

Usage:
    python3 train_mlx.py                    # Run all steps
    python3 train_mlx.py --step split       # Only split data
    python3 train_mlx.py --step train       # Only run LoRA training
    python3 train_mlx.py --step fuse        # Only fuse adapter into base
    python3 train_mlx.py --step convert     # Only convert to GGUF
    python3 train_mlx.py --step create      # Only create Ollama model
    python3 train_mlx.py --test-only        # Evaluate adapter on test set
    python3 train_mlx.py --iters 1000       # Override training iterations
"""

import argparse
import json
import logging
import random
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "aecai_training"
SOURCE_JSONL = DATA_DIR / "aecai_train.jsonl"
TRAIN_JSONL = DATA_DIR / "train.jsonl"
VALID_JSONL = DATA_DIR / "valid.jsonl"
TEST_JSONL = DATA_DIR / "test.jsonl"
ADAPTER_DIR = DATA_DIR / "adapters"
FUSED_DIR = DATA_DIR / "fused_model"
GGUF_PATH = DATA_DIR / "aecai-llama3.gguf"
MODELFILE = DATA_DIR / "Modelfile"
LLAMA_CPP_DIR = Path("/tmp/llama.cpp")

# ---------------------------------------------------------------------------
# Training defaults (tuned for M4 Pro 24 GB)
# ---------------------------------------------------------------------------
BASE_MODEL = "mlx-community/Meta-Llama-3-8B-Instruct-4bit"
DEFAULT_ITERS = 600
BATCH_SIZE = 1
NUM_LAYERS = 8
LEARNING_RATE = 1e-5
SEED = 42

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("train_mlx")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    """Run a subprocess, logging the command and streaming output."""
    log.info("Running: %s", " ".join(str(c) for c in cmd))
    result = subprocess.run(cmd, **kwargs)
    if result.returncode != 0:
        log.error("Command failed with return code %d", result.returncode)
        sys.exit(result.returncode)
    return result


# ---------------------------------------------------------------------------
# Steps
# ---------------------------------------------------------------------------
def step_split():
    """Split aecai_train.jsonl into train / valid / test (80/10/10)."""
    log.info("=== STEP: split ===")

    if not SOURCE_JSONL.exists():
        log.error("Source file not found: %s", SOURCE_JSONL)
        sys.exit(1)

    with open(SOURCE_JSONL) as f:
        examples = [json.loads(line) for line in f if line.strip()]

    log.info("Loaded %d examples from %s", len(examples), SOURCE_JSONL.name)

    random.seed(SEED)
    random.shuffle(examples)

    n = len(examples)
    n_valid = max(1, int(n * 0.10))
    n_test = max(1, int(n * 0.10))
    n_train = n - n_valid - n_test

    splits = {
        TRAIN_JSONL: examples[:n_train],
        VALID_JSONL: examples[n_train : n_train + n_valid],
        TEST_JSONL: examples[n_train + n_valid :],
    }

    for path, data in splits.items():
        with open(path, "w") as f:
            for ex in data:
                f.write(json.dumps(ex) + "\n")
        log.info("Wrote %d examples to %s", len(data), path.name)

    log.info("Split complete: train=%d  valid=%d  test=%d", n_train, n_valid, n_test)


def step_train(iters: int = DEFAULT_ITERS):
    """Run LoRA fine-tuning via mlx_lm.lora."""
    log.info("=== STEP: train (%d iterations) ===", iters)

    for required in (TRAIN_JSONL, VALID_JSONL):
        if not required.exists():
            log.error("Missing %s — run --step split first", required.name)
            sys.exit(1)

    ADAPTER_DIR.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "mlx_lm.lora",
        "--model",
        BASE_MODEL,
        "--train",
        "--data",
        str(DATA_DIR),
        "--batch-size",
        str(BATCH_SIZE),
        "--num-layers",
        str(NUM_LAYERS),
        "--iters",
        str(iters),
        "--learning-rate",
        str(LEARNING_RATE),
        "--adapter-path",
        str(ADAPTER_DIR),
        "--grad-checkpoint",
        "--seed",
        str(SEED),
    ]

    run(cmd)
    log.info("Training complete — adapters saved to %s", ADAPTER_DIR)


def step_test():
    """Evaluate the adapter on the test set."""
    log.info("=== STEP: test ===")

    if not TEST_JSONL.exists():
        log.error("Missing %s — run --step split first", TEST_JSONL.name)
        sys.exit(1)
    if not ADAPTER_DIR.exists():
        log.error("Missing adapters — run --step train first")
        sys.exit(1)

    cmd = [
        sys.executable,
        "-m",
        "mlx_lm.lora",
        "--model",
        BASE_MODEL,
        "--test",
        "--data",
        str(DATA_DIR),
        "--adapter-path",
        str(ADAPTER_DIR),
        "--batch-size",
        str(BATCH_SIZE),
    ]

    run(cmd)
    log.info("Evaluation complete")


def step_fuse():
    """Fuse LoRA adapter into the base model."""
    log.info("=== STEP: fuse ===")

    if not ADAPTER_DIR.exists():
        log.error("Missing adapters — run --step train first")
        sys.exit(1)

    FUSED_DIR.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "mlx_lm.fuse",
        "--model",
        BASE_MODEL,
        "--adapter-path",
        str(ADAPTER_DIR),
        "--save-path",
        str(FUSED_DIR),
        "--dequantize",
    ]

    run(cmd)
    log.info("Fused model saved to %s", FUSED_DIR)


def step_convert():
    """Convert fused HF model to GGUF via llama.cpp."""
    log.info("=== STEP: convert ===")

    if not FUSED_DIR.exists():
        log.error("Missing fused model — run --step fuse first")
        sys.exit(1)

    # Clone llama.cpp if needed
    convert_script = LLAMA_CPP_DIR / "convert_hf_to_gguf.py"
    if not convert_script.exists():
        log.info("Cloning llama.cpp to %s ...", LLAMA_CPP_DIR)
        run(["git", "clone", "--depth", "1", "https://github.com/ggerganov/llama.cpp.git", str(LLAMA_CPP_DIR)])

    # Install llama.cpp Python deps for conversion
    requirements = LLAMA_CPP_DIR / "requirements" / "requirements-convert_hf_to_gguf.txt"
    if requirements.exists():
        run([sys.executable, "-m", "pip", "install", "-q", "-r", str(requirements)])

    # Convert
    cmd = [
        sys.executable,
        str(convert_script),
        str(FUSED_DIR),
        "--outfile",
        str(GGUF_PATH),
        "--outtype",
        "q8_0",
    ]

    run(cmd)
    log.info("GGUF saved to %s", GGUF_PATH)


def step_create():
    """Register the model with Ollama via 'ollama create'."""
    log.info("=== STEP: create ===")

    if not GGUF_PATH.exists():
        log.error("Missing GGUF — run --step convert first")
        sys.exit(1)
    if not MODELFILE.exists():
        log.error("Missing Modelfile at %s", MODELFILE)
        sys.exit(1)

    run(["ollama", "create", "aecai", "-f", str(MODELFILE)])
    log.info("Ollama model 'aecai' created successfully")
    log.info('Test with:  ollama run aecai "Analyze this AEC document..."')


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
STEPS = {
    "split": step_split,
    "train": step_train,
    "fuse": step_fuse,
    "convert": step_convert,
    "create": step_create,
}


def main():
    parser = argparse.ArgumentParser(
        description="AECai MLX LoRA fine-tuning pipeline",
    )
    parser.add_argument(
        "--step",
        choices=list(STEPS.keys()),
        help="Run a single step (default: run all)",
    )
    parser.add_argument(
        "--iters",
        type=int,
        default=DEFAULT_ITERS,
        help=f"Training iterations (default: {DEFAULT_ITERS})",
    )
    parser.add_argument(
        "--test-only",
        action="store_true",
        help="Evaluate adapter on test set and exit",
    )
    args = parser.parse_args()

    if args.test_only:
        step_test()
        return

    if args.step:
        step_fn = STEPS[args.step]
        # Pass iters to train step
        if args.step == "train":
            step_fn(iters=args.iters)
        else:
            step_fn()
        return

    # Run all steps sequentially
    log.info("Running full pipeline")
    step_split()
    step_train(iters=args.iters)
    step_fuse()
    step_convert()
    step_create()
    log.info("Pipeline complete!")


if __name__ == "__main__":
    main()
