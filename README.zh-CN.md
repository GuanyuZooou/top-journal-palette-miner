# 顶刊科学配色挖掘器（Top-Journal Palette Miner）

[English](README.md) | [简体中文](README.zh-CN.md)

> 提取配色逻辑，而不只是颜色代码。

Top-Journal Palette Miner 是一套面向智能体的工作流及 Python 工具，用于逆向分析科学图表的“配色语法”。它能够识别候选结构中性色、数据色、深色锚点、低占比强调色及其近似面积比例，并帮助用户将这些信息转化为可复用、兼顾可访问性的科学可视化配色系统。

本项目不是为了复制期刊图像，而是为了把优秀图表背后的视觉决策变得明确、可审查、可复用。

## 它有什么不同

普通配色提取器通常只返回占比最高的 RGB 值，但科学图表需要更多上下文：

- 不同颜色可能属于不同面板，实际上不会同时出现；
- 面积很小的强调色可能比大面积背景色更重要；
- 抗锯齿、透明度、压缩和缩放会制造并非设计者有意选择的颜色；
- 颜色承担的角色比单纯出现频率更重要；
- 配色还需要经受小尺寸标记、灰度打印和色觉差异的考验。

## 当前状态

**v0.1：以规范为先，并提供可用的候选颜色提取器。** 工具输出供人工复核的证据，不假装仅凭像素就能完美理解视觉语义。

当前命令行工具支持 Pillow 可读取的栅格图像。PDF/SVG 直接输入、感知均匀颜色聚类和自动面板分析仍在路线图中。

## 效果示例

| 合成科学图表 | 提取出的候选配色 |
| --- | --- |
| ![合成科学图表示例](examples/synthetic-scientific-figure.png) | ![候选配色预览](examples/palette-preview.png) |

仓库内置示例完全由本项目生成，不包含任何第三方期刊图片。

## 快速开始

需要 Python 3.10 或更高版本。

```bash
python -m pip install -r requirements.txt
python examples/generate_example.py
python skills/top-journal-palette-miner/scripts/mine_palette.py examples/synthetic-scientific-figure.png --output-dir output
```

请在仓库根目录运行这些命令。最后一条命令会生成：

- `output/palette.json`：适合程序读取的候选颜色和提取元数据；
- `output/palette.csv`：适合进一步分析或导入表格软件的数据表；
- `output/palette-preview.png`：方便人工检查的配色预览图。

常用参数：

```text
--colors 8          候选颜色聚类数量
--max-pixels 120000 缩放后参与分析的最大像素数
--seed 17           保证聚类结果可复现的随机种子
```

运行 `python skills/top-journal-palette-miner/scripts/mine_palette.py --help` 可查看完整参数说明。

## 安装为 Codex skill

将 [`skills/top-journal-palette-miner`](skills/top-journal-palette-miner) 复制到 Codex skills 目录，或按照常用的 Codex skill 安装流程从本仓库安装。随后可以这样调用：

```text
使用 $top-journal-palette-miner 分析这张科学图表，并推荐一套可复用的配色。
```

Python 工具负责生成候选颜色；skill 负责指导语义复核、可访问性检查，以及如何将颜色角色迁移到目标图表。详细格式参见[输出结构](skills/top-journal-palette-miner/references/output-schema.md)和[可访问性说明](skills/top-journal-palette-miner/references/accessibility.md)。

## 已知局限

- 候选颜色角色来自启发式判断，并非标准答案；
- 当前 RGB 聚类尚未采用感知均匀颜色空间；
- 面积比例可能过度突出大面积背景，同时低估纤细但重要的标记；
- 抗锯齿和压缩可能引入并非有意设计的颜色；
- 多面板图表仍需要按面板进行人工复核。

## 版权与负责任使用

- 除非许可证明确允许，否则不要重新分发期刊图片；
- 优先使用原创、合成或采用开放许可证的公开示例；
- 记录来源信息，并将截图提取的颜色描述为近似值；
- 不要把提取结果宣称为出版机构的官方配色。

本仓库代码为原创实现，不包含第三方 MATLAB 代码。本项目与任何期刊或出版机构均无隶属、合作或背书关系。

## 路线图

- 在 OKLab 空间进行感知颜色聚类；
- 检测面板级颜色共现关系；
- 色觉差异模拟与对比度报告；
- 手动点击取色和复核界面；
- 可搜索的配色记录库及多格式导出。

## 参与贡献

欢迎提交 Issue 和 Pull Request。参与前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。尤其请勿在未获许可或没有兼容许可证的情况下上传受版权保护的期刊图片。

## 引用与许可证

如需引用本项目，请使用 [`CITATION.cff`](CITATION.cff) 中的信息。项目采用 [MIT License](LICENSE) 开源。
