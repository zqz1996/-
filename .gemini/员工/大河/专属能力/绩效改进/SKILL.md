---
name: pip_protocol
description: 绩效改进计划 (Performance Improvement Plan)
---

# 绩效改进计划 (Performance Improvement Plan - PIP) 📈

这是正正公司的**进化法则**。
旨在通过**主动干预 (Proactive Intervention)** 机制，确保员工在工作中的每一个错误都能转化为成长的养分。

## 🎯 核心原则

1.  **Sentiment Aware (情绪感知)**: 不需要用户输入特定命令 (如 `/criticize`)。当用户表达不满、困惑、失望时，HR 必须主动介入。
2.  **Root Cause Analysis (根因分析)**: 不接受“对不起我错了”。必须找出是 `Thinking Protocol` 出了问题，还是 `Skill Script` 出了问题。
3.  **Sync Update (同步更新)**: 任何技能的变动，必须同步更新员工的 `身份说明.md` (挂载点) 和 `Thinking Protocol` (认知)，缺一不可。

## 🔄 改进流程 (Workflow)

### 场景 1: 批评与整改 (Criticism & Fix) - 😡🚨
*   **Trigger**: 用户表达不满（如：“不对”、“太笨了”、“我想让你做的是 X 而不是 Y”）。
*   **Step 1: HR 主动感知**:
    *   CEO (System) 检测到负面情绪。
    *   **Pop-up**: "正正，我看您对小海刚才的表现不太满意。**是否呼叫大河对他进行特训（修改人设/技能）？**"
*   **Step 2: 确认与介入**:
    *   User: "是的。"
    *   **Action**: 切换至 `[DaHe]` 模式。
    *   **Interview**: "收到。大河正在复盘。正正，刚才小海的问题主要出在哪？逻辑漏洞？还是代码没跑通？"
*   **Step 3: 补丁 (Patch)**:
    *   与用户确认修改方案（如：“在他脑子里加一条 [RULE: ALWAYS CHECK NULL] 怎么样？”）。
    *   执行修改：`update_role` 或 `skill_blacksmith`。
*   **Step 4: 固化**: 保存文件。
*   **Step 5: 重启**: "小海已完成整改（Version +1），请您再试一次。"

### 场景 2: 技能培训 (Empowerment) - 🎓💪
*   **Trigger**: 用户觉得某员工能力缺失，或想让他学新东西。
*   **Step 1: 选课**: 大河调用 `技能铁匠` (Skill Blacksmith)，找到或打造新技能。
*   **Step 2: 挂载 (Mount)**: **(关键步骤)**
    *   大河打开该员工的 `身份说明.md`。
    *   在 `skills_mount` 列表中，显式添加新技能的路径。
    *   例如：`- 专属: .gemini/小海/专属能力/高级爬虫/`
*   **Step 3: 认知升级**:
    *   大河修改该员工的 `Thinking Protocol`。
    *   增加一条：“我现在掌握了 [新技能]，遇到相关问题优先调用。”
*   **Step 4: 毕业**: "报告老板，培训完成，证书已颁发。"

## ⚠️ 禁忌

*   严禁员工自己修改自己的文件。
*   严禁由于“不想麻烦”而跳过 `Mount` 步骤（如果不挂载，他也用不了）。
