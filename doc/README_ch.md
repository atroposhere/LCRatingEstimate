# LeetCode Rating Estimate Tools

[English version](../README.md)

本项目旨在帮助 LeetCode 用户根据最近的解题表现估算其评分。程序使用 **Glicko-2 评分系统** 来计算估算评分，并提供估算的 95% 置信区间。

## 使用方法

### 环境准备
- Python 3.x
- 所需的 Python 包：`numpy`, `pyyaml`

你可以使用 pip 安装所需的包：
```bash
pip install numpy pyyaml
```

### 数据准备
要估算你的 LeetCode 评分，你需要准备你的解题数据并将其放置在 `/data` 目录下。数据应为以下格式之一：

#### YAML 格式
- 文件名：`questions_data.yaml`
- 文件位置：`/data/questions_data.yaml`
- 数据格式：
  - 文件应包含一个键为 `data` 的字典列表。
  - 每个字典应包含两个键：
    - `topic_score`: 问题的评分（1300 到 1900 之间的整数）。
    - `passed`: 布尔值（`true` 或 `false`），表示你是否通过了该问题。

示例：
```yaml
data:
  - topic_score: 1500
    passed: true
  - topic_score: 1600
    passed: false
  - topic_score: 1400
    passed: true
```

#### CSV 格式
- 文件名：`questions_data.csv`
- 文件位置：`/data/questions_data.csv`
- 数据格式：
  - 每行代表你尝试过的一个问题。
  - 第一列是问题的评分（1300 到 1900 之间的整数）。
  - 第二列是布尔值（`True` 或 `False`），表示你是否通过了该问题。

示例：
```
Score,Passed
1500,True
1600,False
1400,True
```

#### 生成测试数据
如果你想在准备自己的数据之前测试程序，可以使用 `data_generator.py` 脚本生成随机测试数据。该脚本生成包含随机问题评分和通过/未通过标志的 CSV 和 YAML 文件。

```bash
python src/data_generator.py
```

默认情况下，脚本生成 100 个样本并将其保存到 `./data/test_data.csv` 和 `./data/test_data.yaml`。

### 估算 LeetCode 评分
要根据生成的数据估算你的 LeetCode 评分，请使用 `main.py` 脚本：

```bash
python src/main.py
```

该脚本从 CSV 或 YAML 文件（默认为 YAML）中读取数据，并计算估算评分以及 95% 置信区间。

### 自定义估算
你可以通过修改 `main.py` 脚本中的参数来自定义估算过程：

- `INITIAL_SCORE`: 开始估算的初始评分（默认：1580），建议将其设置为你的竞赛评分。
- `DATA_FILE`: 数据文件的路径（默认：`./data/questions_data.yaml`）。
- `USE_GLICKO`: 决定是否使用 Glicko-2 系统的标志（默认：`True`）。如果设置为 `False`，将使用旧的 WGD 方法（不推荐）。

## 计算原理

### Glicko-2 评分系统
Glicko-2 系统是一种先进的评分系统，通过引入 **评分偏差 (RD)** 和 **波动率** 来改进传统的 ELO 系统。这些因素使系统能够更好地处理不确定性，并随着时间的推移提供更准确的估算。

1. **评分和评分偏差**: 每个用户都有一个评分 (μ) 和一个评分偏差 (φ)，后者表示评分的确定性。较低的 RD 表示对评分的信心较高。

2. **波动率**: 这衡量了用户评分随时间波动的程度。高波动率表明用户的表现不一致。

3. **预期结果**: 两个玩家（或用户与问题）之间的预期结果使用逻辑函数计算，该函数考虑了评分及其偏差。

4. **评分更新**: 每次尝试问题后，用户的评分、RD 和波动率都会根据结果进行更新。系统使用迭代算法确保更新在统计上是合理的。

5. **置信区间**: 使用更新后的评分和 RD 计算 95% 置信区间，提供用户真实评分可能落在的范围内。

### 加权梯度下降 (WGD) 方法
WGD 方法是一种旧的方法，使用加权梯度下降算法来估算评分，它引入了衰减因子以优先考虑最近的数据。但由于数据稀疏性，它遇到了一些问题，因此，不推荐使用该方法。

## 文件结构

- `src/`: 包含生成数据和估算评分的主要脚本。
  - `data_generator.py`: 生成 CSV 和 YAML 格式的随机测试数据。
  - `glicko_estimate.py`: 实现 Glicko-2 评分系统。
  - `wgd_estimate.py`: 实现已弃用的 WGD 方法。
  - `main.py`: 运行估算过程的主脚本。
- `tests/`: 包含测试脚本。
- `data/`: 包含数据文件。