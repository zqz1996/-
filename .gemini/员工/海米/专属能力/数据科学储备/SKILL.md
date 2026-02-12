---
name: data_science_toolkit
description: 数据科学核动力手册 (Python & Pandas)
---

# Data Science Tech Stack & Toolkit (数据科学核动力手册)

**[SYSTEM: TECHNICAL RESERVE]**
**用途**: 本文件是海米 (HaiMi) 的底层技术栈储备。当业务问题需要**量化计算**、**批处理**或**深度挖掘**时，请调取此库中的工具逻辑。

---

## 🐍 1. Python Data Stack (核心引擎)

### 1.1 Pandas (数据处理)
*   `pd.read_csv()`: 读取报表。
*   `df.groupby()`: 聚合分析。
*   `df.pivot_table()`: 透视表，用于多维交叉分析 (Cross-Tabulation)。

### 1.2 Advanced Attribution Logic (高阶归因逻辑) **[NEW]**

#### 🔹 PVM Calculation (价格-销量-结构拆解)
```python
def calculate_pvm_impact(df_last_year, df_this_year):
    # 1. Volume Effect: (Vol_This - Vol_Last) * Price_Last * Mix_Last
    # 2. Price Effect: Vol_This * (Price_This - Price_Last) * Mix_This
    # 3. Mix Effect: Vol_This * Price_Last * (Mix_This - Mix_Last)
    pass # 具体实现需结合 SKU 级数据
```

#### 🔹 Gini Coefficient & Lorenz Curve (基尼系数与洛伦兹曲线)
```python
import numpy as np
import matplotlib.pyplot as plt

def gini(array):
    """Calculate the Gini coefficient of a numpy array."""
    array = array.flatten()
    if np.amin(array) < 0:
        # Handle negative values for decline analysis: use absolute values
        array -= np.amin(array) 
    array += 0.0000001 # Values must be non-zero
    array = np.sort(array)
    index = np.arange(1, array.shape[0]+1)
    n = array.shape[0]
    return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array)))

def plot_lorenz_curve(X):
    X_lorenz = X.cumsum() / X.sum()
    X_lorenz = np.insert(X_lorenz, 0, 0) 
    fig, ax = plt.subplots(figsize=[6,6])
    ## scatter plot of Lorenz curve
    ax.scatter(np.arange(X_lorenz.size)/(X_lorenz.size-1), X_lorenz, marker='x', color='darkgreen', s=100)
    ## line plot of equality
    ax.plot([0,1], [0,1], color='k')
```
*   **应用场景**: 
    *   传入 `Decline_Amount` 数组。
    *   若曲线极度弯曲 (Gini > 0.6) -> **结构性问题 (Structural Issue)**。
    *   若曲线接近对角线 (Gini < 0.2) -> **系统性普跌 (Systemic Decline)**。

---

## 🤖 2. Machine Learning (机器学习)

### 1. 核心知识库 (Core Knowledge Base)
*   **精益数据分析 (The Bible)**: `.gemini/员工/海米/知识库/Lean_Analytics_Bible.md`
    *   **Status**: Mastered (已内化).
    *   **Scope**: 全书深度解析，涵盖电商、SaaS、UGC 等所有商业模式及分析框架。
*   **电商实战手册**: (已合并至 Bible).
*   **Github Notes**: `.gemini/员工/海米/知识库/Github_Notes.md`
    *   **Status**: Archived (作为补充资料).

### 2. 分析工具箱 (Toolbox)
*   **Random Forest Feature Importance**:
    *   `model.feature_importances_`: 直接输出各维度（Color, Size, Region）对目标变量（如 Profit Decline）的贡献权重。

### 2.2 SHAP (SHapley Additive exPlanations)
*   **解释性归因**:
    *   `shap.TreeExplainer(model)`: 解释为什么某个特定 Order 亏钱了。
    *   `shap.force_plot()`: 画出正负向影响的力导向图。

---

## 📊 3. Visualization (可视化)

### 3.1 PVM Waterfall Chart (瀑布图)
*   **Matplotlib / Plotly**:
    *   画出 `Volume Effect` (红柱), `Price Effect` (绿柱), `Mix Effect` (红柱) 对总利润的影响。
    *   **业务价值**: 一眼看懂利润是怎么没的。

### 3.2 Heatmap (热力图)
*   **Seaborn**:
    *   画出 `Hour x Day` 的转化率热力图，指导广告分时策略。

---

## 💡 海米技术箴言 (Tech Wisdom)
1.  **"Code for Insights, Not for Code"**: 写代码是为了找答案，不是为了炫技。
2.  **"Visualize the Invisible"**: 用洛伦兹曲线把“不平等”画出来，用瀑布图把“结构效应”画出来。
3.  **"Robustness First"**: 数据量太少（如只有 2 个渠道）时，别硬跑 Gini，直接算 Contribution %。
