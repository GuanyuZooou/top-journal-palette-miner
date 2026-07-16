# Palette record schema

Keep measured values separate from interpretation. Use `unknown` rather than inventing semantics or licensing information.

```json
{
  "algorithm_version": "0.2.0",
  "review_scope": "full-image",
  "source": {"title": "", "url_or_doi": "", "input_type": "screenshot", "licence": "unknown"},
  "colours": [{"hex": "#4D779B", "rgb": [77, 119, 155], "area_fraction": 0.08, "role": "paired-category"}],
  "sub_palettes": [{"name": "paired comparison", "colours": ["#4D779B", "#C45C69"], "panels": ["B"]}],
  "grammar": {"neutral_share": 0.78, "accent_strategy": "one rare warm highlight"},
  "accessibility": {"grayscale": "caution", "colour_vision": "pass", "redundancy": ["marker shape"]},
  "recommended_transfer": {}
}
```

`review_scope` describes what was actually analysed: use `full-image` for one image, `confirmed-panel` for a manually reviewed crop, and `automatic-panel-candidates` only for the output of the panel detector. Preserve the detector's pixel bounds and its annotated PNG alongside any later interpretation. The version field identifies the deterministic extraction implementation, not the publisher's original colour specification.
