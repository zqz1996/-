---
description: 保持工作区整洁，规范临时文件存放位置
---

# Workspace Organization & Temporary File Management

为了保持项目根目录整洁，避免临时脚本和工具文件散落在各处，请遵循以下规则：

1.  **创建专用目录**：
    *   在执行数据处理、临时分析或辅助工具编写时，**必须**首先创建一个专用的子目录（例如 `_scripts`, `_tools`, `temp_processing` 或具体的任务名称目录）。
    *   **禁止**直接在项目根目录 (`.`) 生成非项目核心代码的临时脚本（如 `.py`, `.js`, `.sh` 等一次性脚本）。

2.  **文件存放**：
    *   所有的中间数据文件（如 `.json`, `.csv`, `.xlsx` 副本）也应存放在该专用目录下。
    *   生成的最终产物（Final Artifacts）可以移动到根目录或指定的输出目录，以方便用户查看。

3.  **清理机制**：
    *   任务完成后，询问用户是否保留该临时目录。
    *   如果用户确认不需要，直接删除整个临时目录即可，无需逐个筛选文件。

4.  **示例结构**：
    ```text
    / (Project Root)
    |-- /_scripts           <-- 所有的临时脚本放这里
    |   |-- extract_data.py
    |   |-- convert_format.js
    |   |-- temp_data.json
    |-- core_app.py         <-- 项目核心代码保留在根目录
    |-- output.md           <-- 最终结果保留在根目录
    ```
