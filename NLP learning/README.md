# NLP learning

这是仓库中用于学习与演示自然语言处理（NLP）基础概念的 Jupyter notebooks 集合，主要使用 NLTK（英文处理）和 jieba（中文分词）。下面对每个 notebook 的功能做了简要说明，并包含运行所需的依赖与常见问题解决方法。

## 包含的文件（及说明）

- `NLP_token.ipynb`
	- 功能：更聚焦的分词示例，包含 NLTK 的 `word_tokenize` 和 `jieba` 的示例，适合对比英文与中文分词效果。
    - 亮点：已添加一个随机生成中英文混合文本的单元（用于测试）；对 ASCII（英文）片段使用 `nltk.word_tokenize`，对中文片段使用 `jieba.lcut`。

- `NLP_PorterStemmer.ipynb`
	- 功能：展示 PorterStemmer 的用法（词干提取）。
	- 说明：修复了缺失导入的问题，并增加了用于生成 `word_tokens` 的示例单元，确保可以直接运行词干化示例。

- `NLP_stem.ipynb`
	- 功能：展示词形还原（lemmatization），使用 `WordNetLemmatizer`。
	- 说明：Notebook 中已添加对 `wordnet`（以及 `omw-1.4`）资源的检测与自动下载逻辑，运行前无需手动下载。

- `NLP_treebank.ipynb`
	- 功能：演示 POS（词性）标注，使用 Penn Treebank 标签。
	- 说明：已添加自动检测并下载 `averaged_perceptron_tagger`（及 `punkt`）的单元；POS 标签列表已替换为带中文说明和示例的居中 Markdown 表格。

- `NLP_chunking.ipynb`
	- 功能：短语块(chinking/chunking) 演示与树状结构展示。
	- 说明：已将树形显示从 GUI 弹窗（`tree.draw()`）替换为在 notebook 内嵌显示 SVG 的实现，适合 Jupyter 页面内查看。

- `NLP_NER.ipynb`
	- 功能：命名实体识别（NER）示例，包含 `nltk.ne_chunk` 的用法。
	- 说明：已添加自动检测并下载 NE chunker 所需的资源（`maxent_ne_chunker` / `maxent_ne_chunker_tab`）与 `words` 语料；并新增单元以从构建好的 `tree_test` 中提取并按实体类型聚合结果（例如 PERSON、GPE、ORG 等），便于检查是否找到所有实体。

- `NLP_tree.ipynb`
	- 功能：树结构与句法分析的额外示例（按文件名推断）。

- `NLP_deletestop.ipynb`
	- 功能：演示如何移除停用词（stop words）或进行简单的文本预处理（按文件名推断）。

## 运行环境与依赖

- Python 3.8+
- 建议在虚拟环境（venv / conda）中安装依赖。

安装主要 Python 包（在 PowerShell 中运行）：

```powershell
pip install nltk jieba
```

常用 Python 依赖也可以写入 `requirements.txt`（可选）：

```
nltk
jieba
```

## NLTK 数据资源

部分 notebook 需要 NLTK 的数据资源（如 tokenizer、tagger、chunker、wordnet 等）。大多数 notebook 中已经加入了运行时检测与自动下载逻辑，但如果你在运行时仍看到 LookupError，可以在 Python 交互式环境或 notebook 中手动执行：

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

## 如何运行

1. 在该文件夹下启动 Jupyter Lab / Notebook：

```powershell
jupyter lab
# 或
jupyter notebook
```

2. 依次打开需要的 notebook 并按顺序运行单元（从上到下）。

3. 如果某个单元抛出 LookupError，请先运行包含下载逻辑的单元（通常在文件开头）或手动运行上文的 `nltk.download(...)` 命令。

## 快速检查（示例）

- 在 `NLP_NER.ipynb` 中，已添加的最后一个单元会按实体类型打印在 `tree_test` 中找到的所有实体，例如：

```
PERSON: ['Perrotin', 'Schiaparelli']
GPE: ['Nice', 'Lick Observatory']
```

如果你希望把实体保存为 CSV/JSON 或做更复杂的统计（频率、实体去重、上下文抽取），我可以继续为你添加导出单元或辅助函数。

## 后续建议

- 如果你想在本地一次性安装所有 NLTK 资源，可以运行上文列出的 `nltk.download(...)` 列表。
- 如果需要中文实体识别（NER）示例，可以考虑集成第三方库（如 spaCy 的中文模型、Stanza、HanLP），我可以为你示例如何在 notebook 中加入这些模型的用法。

---

如需我把 README 转成英文或生成 `requirements.txt`、或者将实体提取结果导出为 CSV，请告诉我你想要的格式和路径，我会继续修改。 