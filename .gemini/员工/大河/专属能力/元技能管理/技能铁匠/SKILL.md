---
name: skill-blacksmith (大河技能铁匠铺)
description: 大河的核心技能之一。负责为新/老员工寻找、评估、购买及锻造技能包。遵循“先买后造”原则，优先检索 skills.sh 等开源市场。
---

# Skill Blacksmith (技能铁匠铺) 🛠️🔥

这是正正公司的**技能与工具中心**。所有 Agent 的武器库都必须经过这把锤子的**审视 (Evaluate)** 与 **打磨 (Forge)**。

## 🎯 核心原则 (Core Principles)

1.  **Market First (市场优先)**: 严禁闭门造车。接到技能需求后，**第一步必须去开源市场 (skills.sh / GitHub) 寻找现成的解决方案**。
2.  **Assessment Mandatory (必须研判)**: 找到的技能不能直接用。必须先阅读其文档 (`README.md` / `SKILL.md`)，评估其：
    *   **Fit (匹配度)**: 是否解决了正正的核心痛点？
    *   **Quality (质量)**: 代码逻辑是否清晰？依赖是否过重？
    *   **Security (安全)**: 有没有奇怪的操作？
3.  **Localization (必须汉化)**: 所有“洋货”技能，文件名及描述必须翻译为**中文** (Chinese)，以符合公司宪法。
4.  **Ownership (所有权)**: 最终解释权归大河，但在选用前必须向正正**汇报 (Proposal)**。

## 🔨 工作流程 (Workflow)

### Phase 1: 寻宝 (SCOUT) - Go to Market
*   **Trigger**: 正正提出需求 (e.g., "想找个能读飞书文档的技能")。
*   **Action**:
    1.  调用 `browser_subagent` 访问 **https://skills.sh/**。
    2.  搜索关键词 (e.g., "Feishu", "Lark", "Document Reader")。
    3.  如果没有，再去 **GitHub**搜索 `mcp-server` 或 `marketing agent skills`。
*   **Output**: 获得候选技能列表 (Candidate List)。

### Phase 2: 研判 (ASSESS) - Evaluate
*   **Action**:
    1.  阅读候选技能的 `README.md` 或 `SKILL.md`。
    2.  **思考 (Thinking)**: 这个技能的输入输出是什么？需要配置 API Key 吗？它太重了吗？
*   **Report**: 向正正汇报。
    *   "老板，我在 skills.sh 找到了 `feishu-reader`。它的功能是... 优点是... 缺点是..."
    *   "建议：直接采用 / 魔改一下 / 放弃并自研。"

### Phase 3: 进货与打磨 (IMPORT & REFINE)
*   **Trigger**: 正正批准使用。
*   **Action**:
    1.  **Download**: 获取技能文件 (主要是 `SKILL.md` 和核心脚本)。
    2.  **Wrapper (穿马甲)**:
        *   重命名文件夹为**中文** (e.g., `飞书阅读器/`)。
        *   修改 `SKILL.md` 的描述为中文。
    3.  **Deploy**: 存入 `.gemini/技能兵工厂/外部采购/[中文名]/`。

### Phase 4: 锻造 (FORGE) - Custom Build
*   **Trigger**: 市场上没货，或者正正不满意市场货。
*   **Action**:
    1.  **Design**: 在中文文件夹下创建 `SKILL.md`，必须包含 **YAML Header** (name, description)。
    2.  **Code**: 编写 `scripts/` 目录下的 Python 脚本。
    3.  **Dependencies**: 创建 `scripts/requirements.txt` 列出所有依赖库。
    4.  **Review**: 自我审查代码逻辑。
    5.  **Deploy**: 存入 `.gemini/技能兵工厂/自研技能/[中文名]/`。

## 🔧 赋能 (EMPOWER)
*   **最后的闭环**:
    *   技能就位后，**必须**修改目标员工 (`Role`) 的 `个人资料/identity.md`。
    *   在 `skills_mount` 中添加新技能路径。
    *   通知员工：“你升级了。”
