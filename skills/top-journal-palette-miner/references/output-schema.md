# Palette record schema

Keep measured values separate from interpretation. Use `unknown` rather than inventing semantics or licensing information.

```json
{
  "source": {"title": "", "url_or_doi": "", "input_type": "screenshot", "licence": "unknown"},
  "colours": [{"hex": "#4D779B", "rgb": [77, 119, 155], "area_fraction": 0.08, "role": "paired-category"}],
  "sub_palettes": [{"name": "paired comparison", "colours": ["#4D779B", "#C45C69"], "panels": ["B"]}],
  "grammar": {"neutral_share": 0.78, "accent_strategy": "one rare warm highlight"},
  "accessibility": {"grayscale": "caution", "colour_vision": "pass", "redundancy": ["marker shape"]},
  "recommended_transfer": {}
}
```
