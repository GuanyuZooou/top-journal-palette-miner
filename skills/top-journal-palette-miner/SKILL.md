---
name: top-journal-palette-miner
description: Reverse-engineer the colour grammar of scientific figures, including structural neutrals, semantic accents, panel-level sub-palettes, approximate area shares, colour roles, accessibility risks, and palette transfer recommendations. Use when analysing a journal figure, screenshot, exported panel, or folder of figures to extract reusable scientific-visualisation palettes rather than a flat list of RGB values.
---

# Top-Journal Palette Miner

Extract the colour logic, not just the colour codes.

## Workflow

1. Establish the source and intended reuse. Record whether the input is a screenshot, PDF render, original export, or crop. Treat screenshot colours as approximate.
2. Inspect panels separately when possible. For a raster multi-panel figure with white gutters, first run `scripts/analyze_panels.py`; inspect its annotated rectangles and correct crops manually when needed. Do not infer one global palette when colours occur in different panels.
3. Run `scripts/mine_palette.py` on each confirmed image or panel to obtain candidate colours, area shares, neutral/accent labels, and a preview.
4. Review candidates visually. Merge anti-aliased or compression-derived variants; retain small, saturated accents even when their area is low.
5. Infer roles from geometry and context: axes/text, background data, paired categories, ordered series, reference, uncertainty, or exceptional highlight.
6. Test the proposed sub-palette for grayscale contrast, colour-vision robustness, small-mark visibility, and print suitability.
7. Transfer roles to the target figure. Preserve hierarchy and relationships; do not copy every mined colour into one plot. In Palette Lab's Transfer mode, ask the researcher for figure type, important-series count, and optional emphasis intent; do not infer scientific importance from pixels.
8. Export a concise palette record with provenance, uncertainty, roles, sub-palettes, and recommended uses.

## Run the extractor

Install dependencies if unavailable:

```bash
python -m pip install Pillow numpy
```

Run:

```bash
python scripts/mine_palette.py input.png --output-dir palette-output --colors 8
```

The script writes `palette.json`, `palette.csv`, and `palette-preview.png`. It performs deterministic RGB clustering after downsampling, then labels candidates using luminance, chroma, and area heuristics. Treat labels as evidence for review, not ground truth.

For a multi-panel raster figure, produce an auditable first pass before mining individual panels:

```bash
python scripts/analyze_panels.py figure.png --output-dir panel-output --colors 6
```

This writes `panel-analysis.json` and `panels-annotated.png`. The detector searches for near-white separator bands, so it works best on exported figures with white gutters. It does not understand scientific layout: review every outlined rectangle, especially when panels touch, use a tinted background, or contain large white regions.

## Analyse colour grammar

Separate these systems before recommending reuse:

- **Structural neutrals:** background, axes, typography, grids, context data.
- **Categorical colours:** equal-status groups; prefer similar perceptual weight.
- **Paired colours:** two conceptually linked groups; preserve balanced contrast.
- **Sequential colours:** ordered magnitude; require monotonic lightness.
- **Diverging colours:** deviation around a meaningful midpoint; verify midpoint neutrality.
- **Semantic accents:** rare, high-salience marks for references, events, or exceptions.
- **Dark anchors:** totals, primary response, or figure-wide emphasis.

Infer co-occurrence at panel level. A colour present elsewhere on the page is not automatically available to a given panel's palette.

## Guard against extraction errors

- Prefer original PNG, SVG, or PDF renders over JPEG screenshots.
- Avoid sampling line edges, transparency blends, shadows, and rescaled text.
- Treat near-white pixels as background unless visibly encoded.
- Do not discard rare saturated colours solely because they occupy little area.
- Report approximate values and extraction settings.
- Record `algorithm_version` and `review_scope`; a candidate panel split is not a confirmed semantic interpretation.
- Never claim the sampled value is the publisher's original specification.

## Transfer to a target figure

Map scientific meaning to roles before assigning HEX values. Recommend the smallest sufficient sub-palette and add non-colour redundancy such as marker shapes, line styles, labels, or hatching.

For v0.3a, use deterministic suggestions only: select reference candidates already labelled as data colours, limit them to the requested series count, and emit a warning rather than generating colours when there are too few. Assign a rare accent only once and only to the researcher-specified emphasis. Treat target pixels as evidence for potential simplification, never as proof of scientific semantics. Export `transfer.json`, a readable report, and CSS variables for review.

Use `references/output-schema.md` for a durable palette-library record. Use `references/accessibility.md` for accessibility review and reporting.

## Copyright and attribution

Use published figures as design references, not content to reproduce. Do not redistribute source figures without permission or a compatible licence. Store bibliographic or URL provenance, but publish only original demonstrations, licensed examples, and derived analysis permitted by applicable law and terms.
