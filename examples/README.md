# Examples / 示例

The synthetic figure in this directory is generated locally and contains no third-party journal artwork. From the repository root, run:

本目录中的合成图由项目在本地生成，不包含任何第三方期刊图片。请在仓库根目录运行：

```bash
python examples/generate_example.py
python skills/top-journal-palette-miner/scripts/mine_palette.py examples/synthetic-scientific-figure.png --output-dir output
```

The committed [`palette-preview.png`](palette-preview.png) is generated with the extractor's default settings and is included for README display and visual comparison.

仓库中的 [`palette-preview.png`](palette-preview.png) 使用提取器默认参数生成，用于 README 展示和视觉对照。

To regenerate the three larger original gallery figures, run:

如需重新生成三张更大的原创图库案例图，请运行：

```bash
python examples/generate_gallery.py
```

See [`ASSETS.md`](ASSETS.md) for provenance information and the rule for future licensed third-party examples.

Four openly licensed publication cases live in [`licensed-figures/`](licensed-figures/). They are separate from the original/synthetic assets and are governed by the attribution and CC BY 4.0 records in their case metadata, not by the repository MIT License. Regenerate their analysis outputs with:

```bash
python examples/generate_licensed_case_outputs.py
```
