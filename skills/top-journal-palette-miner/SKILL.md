---
name: top-journal-palette-miner
description: Reverse-engineer the colour grammar of scientific figures, including structural neutrals, semantic accents, panel-level sub-palettes, approximate area shares, colour roles, accessibility risks, and palette transfer recommendations. Use when analysing a journal figure, screenshot, exported panel, or folder of figures to extract reusable scientific-visualisation palettes rather than a flat list of RGB values.
---

# Top-Journal Palette Miner

Extract the colour logic, not just the colour codes.

## Workflow

1. Establish the source and intended reuse. Record whether the input is a screenshot, PDF render, original export, or crop. Treat screenshot colours as approximate.
2. Inspect panels separately when possible. Do not infer one global palette when colours occur in different panels.
3. Run `scripts/mine_palette.py` on each image to obtain candidate colours, area shares, neutral/accent labels, and a preview.
4. Review candidates visually. Merge anti-aliased or compression-derived variants; retain small, saturated accents even when their area is low.
5. Infer roles from geometry and context: axes/text, background data, paired categories, ordered series, reference, uncertainty, or exceptional highlight.
6. Test the proposed sub-palette for grayscale contrast, colour-vision robustness, small-mark visibility, and print suitability.
7. Transfer roles to the target figure. Preserve hierarchy and relationships; do not copy every mined colour into one plot.
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
- Never claim the sampled value is the publisher's original specification.

## Transfer to a target figure

Map scientific meaning to roles before assigning HEX values. Recommend the smallest sufficient sub-palette and add non-colour redundancy such as marker shapes, line styles, labels, or hatching.

Use `references/output-schema.md` for a durable palette-library record. Use `references/accessibility.md` for accessibility review and reporting.

## Copyright and attribution

Use published figures as design references, not content to reproduce. Do not redistribute source figures without permission or a compatible licence. Store bibliographic or URL provenance, but publish only original demonstrations, licensed examples, and derived analysis permitted by applicable law and terms.
