---
name: skill-blacksmith (大河技能铁匠铺)
description: 大河的核心技能之一。负责为新/老员工寻找、购买、汉化或锻造合适的技能包。包含“赋能 (Empower)”与“集权整改”机制。
---

# Skill Blacksmith (技能铁匠铺) 🛠️🔥

这是正正公司的**技能中心及其进化法则**。所有 Agent 所使用的工具都必须经过这把锤子的敲打。

## 🎯 核心原则

1.  **Mandatory Wrapper (强制中文马甲)**: 所有技能（无论自研还是外部采购），其文件夹名称必须使用**从中文 (Chinese)** 命名，以便正正快速检索（如 `网页浏览器/`，而非 `web-browser/`）。核心文件仍为 `SKILL.md`。
2.  **Priority: Buy > Build** (先买后造): 永远优先去 Vercel 市场寻找成熟的解决方案。
3.  **Mandatory Localization** (必须汉化): 所有买回来的“洋货”，必须经过中文润色。
4.  **Strict Isolation** (严格隔离): 技能挂载必须由 HR 执行，普通员工只能“读”。

## 🔨 工作模式 (Work Modes)

### Mode 1: 寻宝 (SCOUT) - Vercel Market
*   **Action**: 调用 `npx skills find [keywords]`。
*   **Output**: 向正正汇报：“老板，市场上找到了这 3 把剑：...”

### Mode 2: 进货与汉化 (IMPORT & LOCALIZE)
*   **Trigger**: 正正选中了某个外部技能（如 `web-browser`）。
*   **Step 1**: Download (`npx skills add ...`).
*   **Step 2**: **Wrapper (穿马甲)**:
    *   根据英文名和描述，给该技能取一个得体、直观的**中文文件夹名**（如 `网页浏览器`）。
    *   重命名下载的目录。
*   **Step 3**: Translate (翻译 `SKILL.md` 内容为中文).
*   **Step 4**: Deploy (保存到 `.gemini/技能兵工厂/外部采购/[中文名]/SKILL.md`).

### Mode 3: 锻造 (FORGE) - Custom Build
*   **Trigger**: 当市场上没有合适的货时。
*   **Standard**: `SKILL.md` + `scripts/` + `examples/` 全套。
*   **Directory Name**: **必须使用中文**（如 `周报生成器/`）。
*   **Target**: 存放在 `.gemini/技能兵工厂/自研技能/[中文名]/`。

### Mode 4: 赋能与整改 (EMPOWER & FIX) 🎓🔧
*   **Scenario**: “给小海加个技能” 或 “小海刚才做错了，给我改！”。
*   **MANDATORY CHECKLIST (必须执行)**:
    1.  **Mount New Skill**:
        *   打开目标员工 (`Role`) 的 `个人资料/identity.md`。
        *   在 `skills_mount` 列表中，**显式添加** 新技能的路径。
        *   例如：`- 专属: .gemini/小海/专属能力/高级爬虫/`
    2.  **Update Thinking**:
        *   打开该员工的 `身份说明.md` (思维协议部分)。
        *   增加认知：“我会用 [新技能] 了。”
    3.  **Confirm**: 保存文件。

## 🚀 交互工作流

1.  **Request**: "大河，给小海加个技能。" / "大河，批评小海。"
2.  **Process**: 找到技能 / 确定错误根因。
3.  **Action**: **必须同步修改 `个人资料/identity.md` (Mount + Thinking)**。
4.  **Result**: "搞定！小海已升级 / 已修正。"
