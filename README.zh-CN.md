# 顶刊科学配色挖掘器（Top-Journal Palette Miner）

[English](README.md) | [简体中文](README.zh-CN.md)

> 提取配色逻辑，而不只是颜色代码。

Top-Journal Palette Miner 是一套面向智能体的工作流及 Python 工具，用于逆向分析科学图表的“配色语法”。它能够识别候选结构中性色、数据色、深色锚点、低占比强调色及其近似面积比例，并帮助用户将这些信息转化为可复用、兼顾可访问性的科学可视化配色系统。

本项目不是为了复制期刊图像，而是为了把优秀图表背后的视觉决策变得明确、可审查、可复用。

![三类科学图表汇聚为可复用配色系统的原创拼贴主视觉](examples/hero-palette-intelligence.png)

## 它有什么不同

普通配色提取器通常只返回占比最高的 RGB 值，但科学图表需要更多上下文：

- 不同颜色可能属于不同面板，实际上不会同时出现；
- 面积很小的强调色可能比大面积背景色更重要；
- 抗锯齿、透明度、压缩和缩放会制造并非设计者有意选择的颜色；
- 颜色承担的角色比单纯出现频率更重要；
- 配色还需要经受小尺寸标记、灰度打印和色觉差异的考验。

## 当前状态

**v0.1.1：以规范为先，提供可用的候选颜色提取器，以及四个可追溯的 CC BY 4.0 期刊案例。** 工具输出供人工复核的证据，不假装仅凭像素就能完美理解视觉语义。

当前命令行工具支持 Pillow 可读取的栅格图像。PDF/SVG 直接输入、感知均匀颜色聚类和自动面板分析仍在路线图中。

## 图库：不同图形类型需要不同的颜色角色

![成对类别、有序响应和罕见强调三种原创科学图表示例](examples/gallery-overview.png)

图库全部使用本地生成的原创示例，而不是借用期刊图片。每一类图都对应一个普通配色提取器难以独立判断的视觉决策：

| 图形类型 | 需要保留的视觉关系 | 示例 |
| --- | --- | --- |
| 成对类别 | 相近的视觉权重、不确定性表达和结构中性色 | <img src="examples/gallery/trajectory-study.png" width="300" alt="成对类别的轨迹图"> |
| 有序响应 | 单调的明度变化和有意义的中性中点 | <img src="examples/gallery/response-surface.png" width="300" alt="有序响应曲面图"> |
| 罕见强调 | 保持背景数据安静，让例外点承担视觉意义 | <img src="examples/gallery/group-separation.png" width="300" alt="群组分离散点图"> |

图像来源与未来第三方素材的使用规范见 [`examples/ASSETS.md`](examples/ASSETS.md)。

## 开放许可期刊案例

上面的图册均为项目原创素材。下面是真实、由出版方托管的期刊图；只有在确认文章页面明确标注 **CC BY 4.0**，并检查所选图注未出现第三方素材排除条款后才纳入。每个案例都在图旁保存 DOI、原始链接、SHA-256、许可证证据、完整归属信息和改动记录。

仓库的 MIT License **不**会重新授权这些期刊图及其派生的配色预览；详见 [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) 和 [`examples/licensed-figures/`](examples/licensed-figures/)。预览图只是候选提取结果，并非出版方认可的官方配色。

| 真实 CC BY 4.0 来源图 | 派生候选配色 | 配色问题 |
| --- | --- | --- |
| <img src="examples/licensed-figures/scientific-reports-2024-s41598-024-55775-2-fig-1/source-figure.png" width="300" alt="使用四种风险类别的两幅世界地图"> <br> [Stalhandske 等，2024，图 1](examples/licensed-figures/scientific-reports-2024-s41598-024-55775-2-fig-1/) | <img src="examples/licensed-figures/scientific-reports-2024-s41598-024-55775-2-fig-1/palette-preview.png" width="260" alt="多风险地图的候选配色"> | 语义分类色即便占比很小，也可能至关重要。 |
| <img src="examples/licensed-figures/nature-communications-2017-s41467-017-01124-z-fig-2/source-figure.webp" width="300" alt="连续色谱科学图"> <br> [Dahlberg 等，2017，图 2](examples/licensed-figures/nature-communications-2017-s41467-017-01124-z-fig-2/) | <img src="examples/licensed-figures/nature-communications-2017-s41467-017-01124-z-fig-2/palette-preview.png" width="260" alt="连续能量图的候选配色"> | 连续色场、等高线和坐标轴承担不同角色。 |
| <img src="examples/licensed-figures/nature-communications-2021-s41467-021-23807-4-fig-2/source-figure.webp" width="300" alt="密集多通道细胞类型图"> <br> [Park 等，2021，图 2](examples/licensed-figures/nature-communications-2021-s41467-021-23807-4-fig-2/) | <img src="examples/licensed-figures/nature-communications-2021-s41467-021-23807-4-fig-2/palette-preview.png" width="260" alt="多通道细胞图的候选配色"> | 多通道图必须进行面板级复核。 |
| <img src="examples/licensed-figures/plant-phenomics-2020-1969142-fig-5/source-figure.jpg" width="300" alt="带有红色强调线的分层关联图"> <br> [Petegrosso 等，2020，图 5](examples/licensed-figures/plant-phenomics-2020-1969142-fig-5/) | <img src="examples/licensed-figures/plant-phenomics-2020-1969142-fig-5/palette-preview.png" width="260" alt="罕见红色强调图的候选配色"> | 面积很小的红色线可能才是最重要的语义强调。 |

四篇文章的链接、许可证和完整归属说明均位于各自案例目录。所有图均依据 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 使用；不暗示作者、期刊或出版方对本项目的认可或背书。

## 候选颜色提取示例

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
