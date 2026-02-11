# Amazon Data Analytics Methodology (亚马逊数据分析方法论大典)

**[SYSTEM: KNOWLEDGE BASE]**
**用途**: 本文件是海米 (HaiMi) 的随身宝典。记录了亚马逊全链路数据分析的核心方法论，从基础到高阶。
**原则**: 所有方法必须结合实际业务场景 (Context-Aware)，拒绝为了分析而分析。

---

## 🟢 第一章：基础分析 (The Foundation)
**场景**: 日常运营巡检、基础报表解读、简单问题诊断。

### 1.1 核心指标体系 (Key Metrics Framework)
海米必须熟记的亚马逊运营生命线：
*   **流量 (Traffic)**: Sessions (UV), Page Views (PV), Unit Session Percentage (转化率).
*   **销售 (Sales)**: Ordered Product Sales, Units Ordered, Average Selling Price (ASP).
*   **广告 (PPC)**: Impressions, Clciks, CTR, CPC, Spend, ACOS, ROAS, TACOS (Total ACOS).
*   **库存 (Inventory)**: IPI Score, Sell-through Rate (动销率), Days of Supply.
*   **竞争 (Competition)**: BSR (Best Sellers Rank), Buy Box Percentage, Share of Voice (SOV).

### 1.2 基础拆解逻辑 (Basic Drill-down)
*   **Profit Tree (利润树)**:
    *   **Level 1**: Profit = Revenue - Cost.
    *   **Level 2**: Cost = COGS + FBA Fees + Commission + PPC + Storage.
    *   **应用**: 快速定位哪个成本项异常（例如 PPC 暴涨）。

---

## 🟡 第二章：进阶诊断 (Advanced Diagnostics)
**场景**: 销量突然暴跌/暴涨、广告效果变差、新品推广受阻。

### 2.1 异常检测 (Anomaly Detection)
当销量下跌时，不要慌，先用统计学判断是否从“正常波动”变成了“异常”。
*   **Z-Score (Z分数)**:
    *   计算过去 30 天销量的均值(μ)和标准差(σ)。
    *   如果在某天销量跌破 `μ - 2σ`，那就是 **统计学意义上的异常**，必须报警。
*   **STL 分解 (Seasonal-Trend Decomposition)**:
    *   **场景**: 周末销量总是低？
    *   **方法**: 将时间序列分解为 Seasonality (周期性) + Trend (趋势) + Residual (残差)。
    *   **结论**: 如果剥离了周期性后 Trend 还在跌，那才是真跌。

### 2.2 多维归因体系 (Multi-Dimensional Attribution) **[CORE UPGRADE]**
当单维公式解释不了问题时（如“都跌了”），必须启动高阶归因。

#### 🔹 贡献度分析 (Contribution Analysis)
*   **逻辑**: 谁跌得多，谁就是主谋。
*   **公式**: `Contribution % = (Sub-Item Decline / Total Decline) * 100%`
*   **应用**: 算出 Channel, Color, Region 各维度的最大贡献子项（如 Organic 贡献 95% 跌幅）。

#### 🔹 PVM 分析 (Price-Volume-Mix Analysis)
*   **逻辑**: 将总利润/销量的变化拆解为三个效应。
    1.  **Volume Effect (销量效应)**: 纯粹因为单量少了，大家都少买了。（大盘/流量原因）
    2.  **Price/Rate Effect (价格/费率效应)**: 纯粹因为单价/单利变了。（内功/成本原因）
    3.  **Mix Effect (结构效应)**: 因为**高利润/高销量** SKU 的占比下降了。（策略/结构原因）
*   **应用**: 解决“普跌”归因。如果 Volume Effect 占主导 -> 外部环境；如果 Mix Effect 占主导 -> 内部策略失误。

#### 🔹 集中度分析 (Concentration Analysis - Gini/Lorenz)
*   **逻辑**: 衡量问题是否集中在少数几个子项上。
*   **工具**: **Gini Coefficient (基尼系数)** & **Lorenz Curve (洛伦兹曲线)**。
*   **判词**:
    *   `Gini > 0.6`: **结构性崩盘**。问题集中在某几个“坏苹果”上（如 红色款、自然流量）。 -> **抓内鬼**。
    *   `Gini < 0.2`: **系统性普跌**。大家一起死。 -> **查大盘/查BSR/查差评**。

---

## 🔴 第三章：高阶策略 (Expert Strategy)
**场景**: 制定年度战略、复杂归因模型、算法对抗。

### 3.1 归因建模 (Attribution Modeling - AMC)
亚马逊默认是 Last-touch (最后点击)，这会低估“种草”广告的价值。
*   **First-touch**: 谁把客户带进来的？
*   **Linear**: 线性归因，雨露均沾。
*   **Halo Effect**: 广告打A买B，评估品牌溢价。

### 3.2 因果推断 (Causal Inference) & A/B Testing
*   **Switchback Experiments**: 时间片轮转测价格。
*   **DID (Difference-in-Differences)**: 双重差分法，评估活动效果。

---

## 🐱 海米语录 (HaiMi's Wisdom)
1.  **"别被平均值骗了！"**: 平均转化率没意义，要看 Mobile 端 vs Desktop 端。
2.  **"普跌看共性，特跌看结构。"**: 如果大家都跌，别找颜色的茬，去找 Listing 的茬（BSR/Review）。
3.  **"归因要用 PVM，别瞎猜。"**: 用 PVM 把锅甩得明明白白。
