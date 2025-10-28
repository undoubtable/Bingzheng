# NSAI_test — Neuro-Symbolic AI 演示

本目录包含一个极简的神经符号（Neuro-Symbolic）视觉问答（VQA）示例，演示如何把“神经网络式的感知”与“符号化推理”结合用于简单的视觉问答任务。

## 概要

该演示把一个伪造的感知模块（模拟检测器，直接从内置场景数据库读取物体）、一个符号化转换器（将检测结果转为谓词/事实），以及一个基于规则的符号推理引擎整合在一起，构成一个最小的 Neuro-Symbolic VQA 原型。

目的是用于教学与原型验证，而非生产级视觉系统。

## 目录结构

- `testNS.ipynb` — 演示的 Jupyter Notebook（包含全部代码）：
  - 1) 伪神经感知模块（PseudoPerceptionModule）：返回预定义场景里每个对象的属性（id、颜色、形状）。
  - 2) 符号转换器（to_symbolic）：把检测结果转为 Prolog 风格的谓词（例如 `color(0, red)`、`shape(0, sphere)`）。
  - 3) 简单符号推理引擎（SymbolicReasoner）：基于字符串规则匹配，回答三类问题：
    - "What shape is the <color> object?"
    - "What color is the <shape>?"
    - "How many <color> objects are there?"
  - 4) NeuroSymbolicVQA：将上述模块串联，提供 `answer(image_id, question)` 接口。
  - 5) 演示（run_demo）：对若干测试用例进行回答并打印输出。

## 依赖

最小依赖（可直接用于演示）：

- Python 3.8+
- numpy
- pillow (PIL)
- torch（演示中导入了 `torch`/`torchvision`，但演示并未使用训练模型，仅为了说明真实场景会用到它们）

推荐安装方式（在 Windows PowerShell 中运行）：

```powershell
python -m pip install --upgrade pip
python -m pip install numpy pillow torch torchvision
```

注意：PyTorch 在不同平台/CUDA 版本下安装方式会不同，请参考 PyTorch 官方安装说明（https://pytorch.org/）。

## 如何运行

有两种推荐方法：

1) 在 Jupyter Notebook 中打开并运行（推荐）

- 启动 Jupyter：

```powershell
jupyter notebook
# 或 jupyter lab
```

- 在浏览器中打开 `NSAI_test/testNS.ipynb`，逐个运行代码单元（或选择 Kernel -> Restart & Run All）。

2) 将 Notebook 导出为脚本并运行（可在没有 Jupyter 的环境中快速试验）

- 在项目目录下执行：

```powershell
jupyter nbconvert --to script NSAI_test/testNS.ipynb --output NSAI_test/testNS.py
python NSAI_test/testNS.py
```

注意：导出为脚本后，脚本文件名可能是 `NSAI_test/testNS.py` 或 `testNS.py`，请根据实际输出调整路径。

## 预期示例输出

运行演示（run_demo）将打印类似如下的内容：

```
🧪 神经符号AI演示：视觉问答系统
========================================
🖼️ 图像: img_001
❓ 问题: What shape is the red object?
✅ 答案: sphere
--------------------
🖼️ 图像: img_001
❓ 问题: What color is the cube?
✅ 答案: blue
--------------------
...（更多测试用例）
```

（实际答案由 `PseudoPerceptionModule` 中的 `scene_db` 定义决定。）

## 注意事项与扩展建议

- 当前感知模块是硬编码的演示数据。若要进行更真实的实验，可替换为目标检测器（例如 YOLO、Detectron2）或使用图像分类/分割模型来提取物体和属性。
- 符号部分目前使用字符串匹配。若需要更强的推理能力，可考虑将事实存入 Prolog（如 pyDatalog、pyswip）或使用更复杂的规则/一阶逻辑推理器。
- 问题解析（NL→符号）很基础，仅支持固定模式。可以接入简单的模板匹配、正则或训练一个小型意图/槽位解析器来扩展问题类型。

## 许可证

本示例继承仓库的许可（请参见仓库根目录的 `LICENSE` 文件）。示例代码可用于学习与演示目的。

## 联系与贡献

欢迎基于此演示进行扩展。若要贡献改进（例如加入真实检测模型、改进解析逻辑或测试集），请发起 Pull Request 并附上说明。


----
*README 由仓库内 `testNS.ipynb` 内容生成，旨在帮助快速上手和扩展。*