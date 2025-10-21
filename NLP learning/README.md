# NLP learning — 仓库说明

这是一个用于学习与演示自然语言处理（NLP）基础概念的 Jupyter notebooks 集合，位于本目录（`NLP learning`）。主要演示英文处理（NLTK）与中文分词（jieba）相关的基础操作、可视化与小型示例脚本。README 目的是帮助你快速了解每个文件的功能、安装依赖、运行方法与常见错误的快速修复。

目录结构（本目录下主要文件）

- `custom_dict.txt` — 自定义词典（用于 jieba 的扩展词表）。
- `stopwords.txt` — 自定义停用词列表（文本预处理示例使用）。
- `requirements.txt` — 推荐的 Python 依赖清单（可直接 pip install -r）。
- `NLP_Chinese.ipynb` — 中文分词示例（jieba）。
- `NLP_chunking.ipynb` — 短语块（chunking/chinking）示例与树形展示（已改为 notebook 内嵌 SVG 渲染）。
- `NLP_deletestop.ipynb` — 文本预处理与停用词移除示例。
- `NLP_NER.ipynb` — 命名实体识别（NER）示例（NLTK 的 `ne_chunk`），包含实体抽取与按类型聚合的示例单元。
- `NLP_PorterStemmer.ipynb` — PorterStemmer（词干提取）示例。
- `NLP_stem.ipynb` — 词形还原（lemmatization）示例，使用 WordNetLemmatizer（包含 wordnet 下载逻辑）。
- `NLP_tokensize.ipynb` — 分词与文本长度（tokenize / size）相关的示例与对比（英文/中文）。
- `NLP_tree.ipynb` — 句法/树结构相关的额外示例（树的构建与渲染）。
- `NLP_treebank.ipynb` — POS（词性）标注示例（已加入 averaged_perceptron_tagger 的检测/自动下载逻辑）。
- `README.md` — 当前文档（你正在阅读的文件）。

每个 notebook 都尽量包含必要的运行前检测（例如 NLTK 数据资源的检测并尝试自动下载），以降低首次运行时的手动准备量。

快速开始（推荐）

1) 建议创建并激活虚拟环境（可选，但推荐）

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2) 安装 Python 依赖（PowerShell）：

```powershell
pip install -r "requirements.txt"
# 或者单独安装
pip install nltk jieba ipython matplotlib
```

3) 启动 Jupyter（在本目录）：

```powershell
jupyter lab
# 或
jupyter notebook
```

4) 打开需要的 notebook（例如 `NLP_treebank.ipynb`），按从上到下顺序运行单元。

NLTK 数据资源（如果遇到 LookupError）

部分 notebook 使用了 NLTK 的外部数据资源（分词器、tagger、chunker、wordnet 等）。大多数 notebook 已经包含了运行时的检测与自动下载逻辑，但如果仍然出现 LookupError，你可以手动在 Python 交互式环境或 notebook 中运行：

```python
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('maxent_ne_chunker_tab')
nltk.download('words')
nltk.download('wordnet')
nltk.download('omw-1.4')
```

常见问题与快速修复

- 问：运行 `nltk.pos_tag` 或 `nltk.ne_chunk` 时出现 LookupError（资源缺失）。
	- 处理：运行上述 `nltk.download(...)` 列表，或在对应 notebook 顶部先运行包含自动下载逻辑的单元。

- 问：在 `NLP_Chinese.ipynb` 中打印出一个 generator 对象而非分词结果。
	- 处理：代码中已将 `jieba.cut(text)` 转为 `list(jieba.cut(text))`，请确保你运行了修正后的单元。

- 问：`tree.draw()` 弹出外部窗口导致在无头环境无法查看。
	- 处理：已将树展示改为在 notebook 内嵌 SVG（使用 `tree._repr_svg_()` + `IPython.display.SVG`），在 Jupyter 页面中直接可见。

- 问：某些可视化依赖（例如第三方增强包）缺失。
	- 处理：这些增强包为可选项（例如 `svgling`）。如果缺少，只影响展示效果，核心功能仍可运行。你可以选择安装：

```powershell
pip install svgling
```

扩展建议和下一步

- 如果你需要将 NER 结果导出：我可以添加一个 notebook 单元，把聚合后的实体保存为 CSV/JSON（示例：按实体类型计数并输出 CSV）。
- 需要中文 NER（识别中文人名/地名/组织）的话，推荐使用 spaCy（中文模型）、Stanza 或 HanLP；这些库可以给出更好的中文 NER 结果。我可以为某一款库写示例集成单元。

文件说明（逐个简短说明）

- `custom_dict.txt` — 可以用来扩展 jieba 的用户词典，使用方法：在 notebook 中调用 `jieba.load_userdict("custom_dict.txt")`。
- `stopwords.txt` — 停用词列表（每行一个词），`NLP_deletestop.ipynb` 演示了如何使用它们进行文本清洗。
- `requirements.txt` — 推荐依赖，已包含基本包（请先安装到虚拟环境中）。
- `NLP_Chinese.ipynb` — 中文分词（jieba）的典型用法：精确模式、全模式、搜索引擎模式，并示例如何处理中英文混合文本。
- `NLP_chunking.ipynb` — chunking/chinking 的例子，并在 notebook 中以 SVG 形式渲染树形结构，便于展示句法成分。
- `NLP_deletestop.ipynb` — 演示了如何加载停用词并从 token 列表中过滤停用词。
- `NLP_NER.ipynb` — NLTK 的 NE 识别示例：包含 `ne_chunk` 的使用、必要数据的自动检测/下载，以及示例单元把实体按类型（PERSON、GPE、ORG 等）聚合并打印。
- `NLP_PorterStemmer.ipynb` — 演示 Porter 词干提取器的用法，包含对输入字符串的分词和词干化结果展示。
- `NLP_stem.ipynb` — 使用 WordNetLemmatizer 的词形还原示例，Notebook 含有对 `wordnet` 和 `omw-1.4` 的下载检查逻辑。
- `NLP_tokensize.ipynb` — 展示 tokenization 后的长度统计、英文/中文分词差异等。
- `NLP_tree.ipynb` — 句法树构造与渲染示例（用于研究 parse/树的构造与展示）。
- `NLP_treebank.ipynb` — POS 标注与 Penn Treebank 标签说明；已包含对 `averaged_perceptron_tagger` 和 `punkt` 的自动下载单元。
