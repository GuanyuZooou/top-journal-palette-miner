#!/usr/bin/env python3
"""Mine candidate colours and approximate roles from a raster figure."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ALGORITHM_VERSION = "0.2.0"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("palette-output"))
    parser.add_argument("--colors", type=int, default=8)
    parser.add_argument("--max-pixels", type=int, default=120_000)
    parser.add_argument("--seed", type=int, default=17)
    return parser.parse_args()


def load_pixels(path: Path, max_pixels: int) -> tuple[np.ndarray, tuple[int, int]]:
    image = Image.open(path).convert("RGB")
    original_size = image.size
    scale = min(1.0, (max_pixels / max(1, image.width * image.height)) ** 0.5)
    if scale < 1:
        image = image.resize(
            (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
            Image.Resampling.LANCZOS,
        )
    return np.asarray(image, dtype=np.float32).reshape(-1, 3), original_size


def kmeans(pixels: np.ndarray, k: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    k = max(1, min(k, len(pixels)))
    centers = [pixels[rng.integers(len(pixels))]]
    nearest = ((pixels - centers[0]) ** 2).sum(axis=1)
    for _ in range(1, k):
        total = nearest.sum()
        if total <= 0:
            centers.append(pixels[rng.integers(len(pixels))])
        else:
            centers.append(pixels[rng.choice(len(pixels), p=nearest / total)])
        nearest = np.minimum(nearest, ((pixels - centers[-1]) ** 2).sum(axis=1))
    centers = np.asarray(centers, dtype=np.float32)
    labels = np.zeros(len(pixels), dtype=np.int32)
    for _ in range(40):
        distances = ((pixels[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        new_labels = distances.argmin(axis=1)
        new_centers = centers.copy()
        for index in range(k):
            members = pixels[new_labels == index]
            if len(members):
                new_centers[index] = members.mean(axis=0)
        if np.array_equal(labels, new_labels) and np.allclose(centers, new_centers, atol=0.2):
            labels, centers = new_labels, new_centers
            break
        labels, centers = new_labels, new_centers
    return np.clip(np.rint(centers), 0, 255).astype(np.uint8), labels


def srgb_luminance(rgb: np.ndarray) -> float:
    values = rgb.astype(float) / 255.0
    linear = np.where(values <= 0.04045, values / 12.92, ((values + 0.055) / 1.055) ** 2.4)
    return float(linear @ np.array([0.2126, 0.7152, 0.0722]))


def classify(rgb: np.ndarray, share: float) -> tuple[str, float, float]:
    values = rgb.astype(float) / 255.0
    chroma = float(values.max() - values.min())
    luminance = srgb_luminance(rgb)
    if luminance > 0.91 and chroma < 0.08:
        role = "background-neutral"
    elif chroma < 0.10:
        role = "structural-neutral"
    elif share < 0.025 and chroma > 0.30:
        role = "rare-accent-candidate"
    elif luminance < 0.16:
        role = "dark-anchor-candidate"
    else:
        role = "data-colour-candidate"
    return role, luminance, chroma


def make_records(centers: np.ndarray, labels: np.ndarray) -> list[dict]:
    counts = np.bincount(labels, minlength=len(centers))
    order = np.argsort(counts)[::-1]
    records = []
    for rank, index in enumerate(order, start=1):
        rgb = centers[index]
        share = float(counts[index] / counts.sum())
        role, luminance, chroma = classify(rgb, share)
        records.append({
            "rank": rank,
            "hex": "#" + "".join(f"{int(value):02X}" for value in rgb),
            "rgb": [int(value) for value in rgb],
            "area_fraction": round(share, 6),
            "candidate_role": role,
            "relative_luminance": round(luminance, 4),
            "rgb_chroma": round(chroma, 4),
        })
    return records


def preview(records: list[dict], path: Path) -> None:
    width, row_height = 760, 86
    canvas = Image.new("RGB", (width, row_height * len(records)), "white")
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.load_default(size=18)
    except TypeError:
        font = ImageFont.load_default()
    for row, record in enumerate(records):
        y = row * row_height
        draw.rounded_rectangle((18, y + 14, 150, y + 70), radius=10, fill=tuple(record["rgb"]), outline="#333333")
        label = f'{record["hex"]}   {record["area_fraction"]:.1%}   {record["candidate_role"]}'
        draw.text((174, y + 31), label, fill="#202020", font=font)
    canvas.save(path)


def main() -> None:
    args = parse_args()
    if args.colors < 1:
        raise SystemExit("--colors must be at least 1")
    pixels, original_size = load_pixels(args.image, args.max_pixels)
    centers, labels = kmeans(pixels, args.colors, args.seed)
    records = make_records(centers, labels)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "algorithm_version": ALGORITHM_VERSION,
        "source": args.image.as_posix(),
        "input_type": "raster",
        "review_scope": "full-image",
        "original_size_px": list(original_size),
        "sampled_pixels": int(len(pixels)),
        "cluster_count": len(records),
        "sampling_note": "Candidate colours are approximate and require visual/semantic review.",
        "colours": records,
    }
    (args.output_dir / "palette.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    with (args.output_dir / "palette.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = [key for key in records[0] if key != "rgb"] + ["rgb"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["rgb"] = ",".join(map(str, record["rgb"]))
            writer.writerow(row)
    preview(records, args.output_dir / "palette-preview.png")
    print(f"Wrote {len(records)} colour candidates.")


if __name__ == "__main__":
    main()
