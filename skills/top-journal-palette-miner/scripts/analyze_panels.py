#!/usr/bin/env python3
"""Detect approximate figure panels and mine a colour grammar for each one.

The detector is intentionally conservative: it looks for near-white separator
bands in a raster figure, rather than claiming to understand a publication's
layout.  It is most useful for exported multi-panel figures with white gutters.
Review the annotated result before treating a rectangle as a semantic panel.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


Rect = tuple[int, int, int, int]
ALGORITHM_VERSION = "0.2.0"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("panel-output"))
    parser.add_argument("--colors", type=int, default=6)
    parser.add_argument("--max-pixels", type=int, default=60_000,
                        help="Maximum sampled pixels per detected panel.")
    parser.add_argument("--max-detection-pixels", type=int, default=1_200_000,
                        help="Downsample very large figures before panel detection.")
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--white-threshold", type=int, default=245,
                        help="RGB values at or above this neutral threshold are background.")
    parser.add_argument("--blank-fraction", type=float, default=0.02,
                        help="Maximum foreground fraction permitted in a separator band.")
    parser.add_argument("--min-panel-size", type=int, default=80,
                        help="Minimum panel side length in input-image pixels.")
    parser.add_argument("--max-panels", type=int, default=16)
    parser.add_argument("--padding", type=int, default=8,
                        help="Pixels retained around detected foreground in each panel.")
    return parser.parse_args()


def _resized_for_detection(image: Image.Image, max_pixels: int) -> Image.Image:
    if max_pixels < 1:
        raise ValueError("max_detection_pixels must be at least 1")
    scale = min(1.0, (max_pixels / max(1, image.width * image.height)) ** 0.5)
    if scale >= 1:
        return image
    return image.resize(
        (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
        Image.Resampling.BILINEAR,
    )


def foreground_mask(rgb: np.ndarray, white_threshold: int) -> np.ndarray:
    """Return pixels that are not an approximately neutral white background."""
    if not 0 <= white_threshold <= 255:
        raise ValueError("white_threshold must be between 0 and 255")
    if rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError("rgb must have shape (height, width, 3)")
    return rgb.min(axis=2) < white_threshold


def _content_bounds(mask: np.ndarray, rect: Rect, padding: int = 0) -> Rect:
    x0, y0, x1, y1 = rect
    local = mask[y0:y1, x0:x1]
    rows = np.flatnonzero(local.any(axis=1))
    columns = np.flatnonzero(local.any(axis=0))
    if not len(rows) or not len(columns):
        return rect
    return (
        max(x0, x0 + int(columns[0]) - padding),
        max(y0, y0 + int(rows[0]) - padding),
        min(x1, x0 + int(columns[-1]) + 1 + padding),
        min(y1, y0 + int(rows[-1]) + 1 + padding),
    )


def _runs(values: np.ndarray) -> list[tuple[int, int]]:
    """Return half-open runs of true values."""
    runs: list[tuple[int, int]] = []
    start: int | None = None
    for index, value in enumerate(values):
        if value and start is None:
            start = index
        elif not value and start is not None:
            runs.append((start, index))
            start = None
    if start is not None:
        runs.append((start, len(values)))
    return runs


def _separator_candidates(
    density: np.ndarray,
    start: int,
    stop: int,
    min_side: int,
    min_gutter: int,
    blank_fraction: float,
) -> list[tuple[float, int]]:
    candidates: list[tuple[float, int]] = []
    for run_start, run_stop in _runs(density <= blank_fraction):
        run_length = run_stop - run_start
        absolute_start = start + run_start
        absolute_stop = start + run_stop
        if run_length < min_gutter:
            continue
        if absolute_start - start < min_side or stop - absolute_stop < min_side:
            continue
        whiteness = 1.0 - float(density[run_start:run_stop].mean())
        candidates.append((run_length * whiteness, (absolute_start + absolute_stop) // 2))
    return candidates


def _has_material_content(mask: np.ndarray, rect: Rect) -> bool:
    x0, y0, x1, y1 = rect
    local = mask[y0:y1, x0:x1]
    return int(local.sum()) >= max(12, int(local.size * 0.002))


def _best_split(
    mask: np.ndarray,
    rect: Rect,
    min_side: int,
    min_gutter: int,
    blank_fraction: float,
) -> tuple[str, int] | None:
    x0, y0, x1, y1 = rect
    local = mask[y0:y1, x0:x1]
    candidates: list[tuple[float, str, int]] = []

    horizontal_density = local.mean(axis=1)
    for score, cut in _separator_candidates(
        horizontal_density, y0, y1, min_side, min_gutter, blank_fraction
    ):
        upper = (x0, y0, x1, cut)
        lower = (x0, cut, x1, y1)
        if _has_material_content(mask, upper) and _has_material_content(mask, lower):
            candidates.append((score, "horizontal", cut))

    vertical_density = local.mean(axis=0)
    for score, cut in _separator_candidates(
        vertical_density, x0, x1, min_side, min_gutter, blank_fraction
    ):
        left = (x0, y0, cut, y1)
        right = (cut, y0, x1, y1)
        if _has_material_content(mask, left) and _has_material_content(mask, right):
            candidates.append((score, "vertical", cut))

    if not candidates:
        return None
    # Stable sort means equal candidates resolve to the earlier geometry order.
    _, orientation, cut = max(candidates, key=lambda item: item[0])
    return orientation, cut


def _split_regions(
    mask: np.ndarray,
    rect: Rect,
    min_side: int,
    min_gutter: int,
    blank_fraction: float,
    max_panels: int,
) -> list[Rect]:
    regions = [rect]
    index = 0
    while index < len(regions) and len(regions) < max_panels:
        region = regions[index]
        split = _best_split(mask, region, min_side, min_gutter, blank_fraction)
        if split is None:
            index += 1
            continue
        orientation, cut = split
        x0, y0, x1, y1 = region
        if orientation == "horizontal":
            children = [(x0, y0, x1, cut), (x0, cut, x1, y1)]
        else:
            children = [(x0, y0, cut, y1), (cut, y0, x1, y1)]
        regions[index:index + 1] = children
    return regions


def _map_rect(rect: Rect, source_size: tuple[int, int], detection_size: tuple[int, int]) -> Rect:
    x0, y0, x1, y1 = rect
    source_width, source_height = source_size
    detection_width, detection_height = detection_size
    return (
        max(0, int(np.floor(x0 * source_width / detection_width))),
        max(0, int(np.floor(y0 * source_height / detection_height))),
        min(source_width, int(np.ceil(x1 * source_width / detection_width))),
        min(source_height, int(np.ceil(y1 * source_height / detection_height))),
    )


def detect_panels(
    image: Image.Image,
    *,
    white_threshold: int = 245,
    blank_fraction: float = 0.02,
    min_panel_size: int = 80,
    max_panels: int = 16,
    padding: int = 8,
    max_detection_pixels: int = 1_200_000,
) -> list[Rect]:
    """Return approximate panel rectangles as ``(left, top, right, bottom)``.

    Coordinates use the input image.  A figure with no detectable white gutter
    is represented by one content-bounded region rather than being over-split.
    """
    if not 0 < blank_fraction < 1:
        raise ValueError("blank_fraction must be between 0 and 1")
    if min_panel_size < 1 or max_panels < 1 or padding < 0:
        raise ValueError("min_panel_size and max_panels must be positive; padding cannot be negative")

    source = image.convert("RGB")
    detection = _resized_for_detection(source, max_detection_pixels)
    mask = foreground_mask(np.asarray(detection), white_threshold)
    detection_width, detection_height = detection.size
    root = (0, 0, detection_width, detection_height)
    if not mask.any():
        return [(0, 0, source.width, source.height)]

    root = _content_bounds(mask, root)
    scale = min(detection_width / source.width, detection_height / source.height)
    min_side = max(4, round(min_panel_size * scale))
    min_gutter = max(2, round(min_side * 0.10))
    padding_detection = max(0, round(padding * scale))
    regions = _split_regions(
        mask, root, min_side, min_gutter, blank_fraction, max_panels
    )
    regions = [_content_bounds(mask, region, padding_detection) for region in regions]
    mapped = [_map_rect(region, source.size, detection.size) for region in regions]
    return sorted(mapped, key=lambda region: (region[1], region[0]))


def _sample_pixels(rgb: np.ndarray, max_pixels: int) -> np.ndarray:
    if max_pixels < 1:
        raise ValueError("max_pixels must be at least 1")
    height, width = rgb.shape[:2]
    scale = min(1.0, (max_pixels / max(1, height * width)) ** 0.5)
    if scale < 1:
        image = Image.fromarray(rgb, mode="RGB").resize(
            (max(1, round(width * scale)), max(1, round(height * scale))),
            Image.Resampling.LANCZOS,
        )
        rgb = np.asarray(image)
    return rgb.astype(np.float32).reshape(-1, 3)


def kmeans(pixels: np.ndarray, k: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Deterministic k-means++ clustering in RGB space."""
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


def colour_records(centers: np.ndarray, labels: np.ndarray) -> list[dict[str, object]]:
    counts = np.bincount(labels, minlength=len(centers))
    order = np.argsort(counts)[::-1]
    records: list[dict[str, object]] = []
    total = max(1, int(counts.sum()))
    for index in order:
        if not counts[index]:
            continue
        rgb = centers[index]
        share = float(counts[index] / total)
        role, luminance, chroma = classify(rgb, share)
        records.append({
            "rank": len(records) + 1,
            "hex": "#" + "".join(f"{int(value):02X}" for value in rgb),
            "rgb": [int(value) for value in rgb],
            "area_fraction": round(share, 6),
            "candidate_role": role,
            "relative_luminance": round(luminance, 4),
            "rgb_chroma": round(chroma, 4),
        })
    return records


def _font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def annotate_panels(image: Image.Image, panels: list[Rect], path: Path) -> None:
    """Save an input-sized figure with deterministic panel labels and outlines."""
    canvas = image.convert("RGB").copy()
    draw = ImageDraw.Draw(canvas)
    width = max(2, round(min(canvas.size) / 350))
    font = _font(max(12, round(min(canvas.size) / 42)))
    colours = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9"]
    for number, (x0, y0, x1, y1) in enumerate(panels, start=1):
        colour = colours[(number - 1) % len(colours)]
        draw.rectangle((x0, y0, max(x0, x1 - 1), max(y0, y1 - 1)), outline=colour, width=width)
        label = f"P{number:02d}"
        box = draw.textbbox((0, 0), label, font=font)
        label_width = box[2] - box[0] + width * 2
        label_height = box[3] - box[1] + width * 2
        label_y = max(0, y0 - label_height)
        draw.rectangle((x0, label_y, x0 + label_width, label_y + label_height), fill=colour)
        draw.text((x0 + width, label_y + width), label, fill="white", font=font)
    canvas.save(path)


def analyse(image_path: Path, args: argparse.Namespace) -> dict[str, object]:
    image = Image.open(image_path).convert("RGB")
    panels = detect_panels(
        image,
        white_threshold=args.white_threshold,
        blank_fraction=args.blank_fraction,
        min_panel_size=args.min_panel_size,
        max_panels=args.max_panels,
        padding=args.padding,
        max_detection_pixels=args.max_detection_pixels,
    )
    image_array = np.asarray(image)
    panel_records: list[dict[str, object]] = []
    for number, (x0, y0, x1, y1) in enumerate(panels, start=1):
        pixels = _sample_pixels(image_array[y0:y1, x0:x1], args.max_pixels)
        centers, labels = kmeans(pixels, args.colors, args.seed + number - 1)
        colours = colour_records(centers, labels)
        panel_records.append({
            "id": f"panel-{number:02d}",
            "bbox_xywh_px": {"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0},
            "sampled_pixels": int(len(pixels)),
            "cluster_count": len(colours),
            "colours": colours,
        })
    return {
        "algorithm_version": ALGORITHM_VERSION,
        "source": image_path.as_posix(),
        "input_type": "raster",
        "original_size_px": [image.width, image.height],
        "panel_count": len(panel_records),
        "review_scope": "automatic-panel-candidates",
        "detection": {
            "method": "near-white separator-band projection",
            "white_threshold": args.white_threshold,
            "blank_fraction": args.blank_fraction,
            "min_panel_size_px": args.min_panel_size,
            "note": "Panel bounds are approximate. Review the annotated PNG before interpretation.",
        },
        "panels": panel_records,
    }


def main() -> None:
    args = parse_args()
    if args.colors < 1:
        raise SystemExit("--colors must be at least 1")
    if args.max_pixels < 1 or args.max_detection_pixels < 1:
        raise SystemExit("pixel limits must be at least 1")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    payload = analyse(args.image, args)
    (args.output_dir / "panel-analysis.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    image = Image.open(args.image).convert("RGB")
    panels = [
        (
            int(panel["bbox_xywh_px"]["x"]),
            int(panel["bbox_xywh_px"]["y"]),
            int(panel["bbox_xywh_px"]["x"] + panel["bbox_xywh_px"]["width"]),
            int(panel["bbox_xywh_px"]["y"] + panel["bbox_xywh_px"]["height"]),
        )
        for panel in payload["panels"]
    ]
    annotate_panels(image, panels, args.output_dir / "panels-annotated.png")
    print(f"Wrote {payload['panel_count']} panel analyses.")


if __name__ == "__main__":
    main()
