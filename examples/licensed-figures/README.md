# Openly licensed publication cases / 开放许可期刊案例

This directory is a small, traceable benchmark for scientific-figure palette analysis. It contains four publisher-hosted figures selected because their article pages explicitly state **CC BY 4.0** and the selected captions show no figure-specific third-party rights exclusion.

这些案例构成一个小型、可追溯的科学图表配色基准。每张图都来自明确标注 **CC BY 4.0** 的文章页面，且所选图注未显示针对该图的第三方权利排除条款。

The repository MIT License does not apply to these assets. Read [`../../THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md) and every case's `metadata.yml` before reuse.

仓库的 MIT 许可证不适用于这些素材。再次使用前，请阅读 [`../../THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md) 与各案例的 `metadata.yml`。

| Case | Journal / figure | Colour question |
| --- | --- | --- |
| [`scientific-reports-2024-s41598-024-55775-2-fig-1`](scientific-reports-2024-s41598-024-55775-2-fig-1/) | *Scientific Reports* (2024), Figure 1 | Are red, blue, purple, and grey categorical states rather than merely frequent pixels? |
| [`nature-communications-2017-s41467-017-01124-z-fig-2`](nature-communications-2017-s41467-017-01124-z-fig-2/) | *Nature Communications* (2017), Figure 2 | How should a continuous heatmap and its neutral background be treated? |
| [`nature-communications-2021-s41467-021-23807-4-fig-2`](nature-communications-2021-s41467-021-23807-4-fig-2/) | *Nature Communications* (2021), Figure 2 | Which colours belong to dense multichannel data versus the page furniture? |
| [`plant-phenomics-2020-1969142-fig-5`](plant-phenomics-2020-1969142-fig-5/) | *Plant Phenomics* (2020), Figure 5 | Can a low-area red annotation be recognised as an intentional emphasis? |

To reproduce every committed analysis output from the repository root:

```bash
python examples/generate_licensed_case_outputs.py
```

The `source-figure.*` files are downloaded official figure renditions. `palette.json`, `palette.csv`, and `palette-preview.png` are generated analytical derivatives; they are not statements by the original authors or publishers.
