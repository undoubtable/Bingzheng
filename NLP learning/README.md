# NLP learning

This folder contains Jupyter notebooks demonstrating tokenization for English and Chinese text using NLTK and jieba.

## Files
- `NLP.ipynb` - Mixed examples: English tokenization with NLTK, Chinese tokenization with jieba, and a cell that generates random mixed Chinese-English text for testing.
- `NLP_token.ipynb` - Tokenization-focused notebook with examples for NLTK and jieba.

## Requirements
- Python 3.8+
- pip

## Install dependencies
Run in PowerShell:

```powershell
pip install nltk jieba
```

After installing, download required NLTK data (inside a Python REPL or from a notebook cell):

```python
import nltk
nltk.download('punkt')
# optionally nltk.download('punkt_tab') if used
```

## How to run
1. Open Jupyter Notebook or JupyterLab in this folder:

```powershell
jupyter notebook
# or
jupyter lab
```

2. Open `NLP.ipynb` and run cells in order. The cell that generates random mixed text will create sample text and then tokenize it using NLTK for English parts and jieba for Chinese parts.

## Notes
- If you see LookupError from NLTK, run the `nltk.download('punkt')` command.
- The random text generator in the notebook uses only Python standard library modules (`random`, `string`) and does not need extra packages.

## Example
Running the mixed-text cell will print a list of tokens produced by a combination of NLTK word_tokenize (for ASCII words) and jieba.lcut (for Chinese segments).