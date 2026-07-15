# Contributing / 参与贡献

Thank you for helping improve Top-Journal Palette Miner. 中文说明见下半部分。

## English

### Before opening an issue

- Search existing issues first.
- For extraction bugs, include the command, Python version, operating system, and the smallest reproducible input you are allowed to share.
- Do not upload copyrighted journal figures unless you have permission or the figure has a compatible licence. A synthetic reproduction is usually better.
- Remove private paths, author metadata, and unpublished research data from logs and examples.

### Development setup

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Please keep extraction deterministic when a seed is supplied, add tests for behavioural changes, and update both README files when user-facing behaviour changes.

### Pull requests

Keep each pull request focused. Describe what changed, why it changed, how it was tested, and whether it affects output compatibility, accessibility guidance, or copyright/provenance handling.

## 中文

### 提交 Issue 前

- 请先搜索已有 Issue，避免重复反馈。
- 如果反馈提取错误，请提供运行命令、Python 版本、操作系统，以及你有权分享的最小复现输入。
- 除非已获得许可或图片采用兼容许可证，否则不要上传受版权保护的期刊图片；通常更推荐制作合成复现示例。
- 请从日志和示例中移除私人路径、作者元数据和未公开研究数据。

### 开发环境

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

提供随机种子时，颜色提取结果应保持可复现。行为发生变化时请补充测试；面向用户的功能发生变化时，请同步更新中英文 README。

### Pull Request

每个 Pull Request 应聚焦一个主题，并说明改了什么、为什么修改、如何验证，以及是否影响输出兼容性、可访问性建议或版权与来源处理。
