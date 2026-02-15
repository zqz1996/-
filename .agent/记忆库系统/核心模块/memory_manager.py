"""
正正公司员工记忆库系统 - 核心模块
Memory Manager for ZhengZheng Corp Employee Memory System

功能：
- 读取/写入员工记忆
- 自动归档（按月）
- 格式验证与修复
- 智能加载（近期详细 + 远期摘要）

作者：正正公司技术团队
版本：1.0.0
"""

import os
import re
import json
import shutil
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class MemoryType(Enum):
    """记忆类型枚举"""
    WORK_LOG = "work_log"      # 工作日志
    RELATION = "relation"      # 人际关系
    LEARNING = "learning"      # 技能经验
    CHAT = "chat"              # 闲聊记录


@dataclass
class MemoryEntry:
    """单条记忆条目"""
    timestamp: str
    date: str
    content: str
    source: str  # 记忆来源（谁写的）
    memory_type: MemoryType
    tags: Optional[List[str]] = None
    importance: int = 3  # 1-5，5最重要
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class MemoryManager:
    """
    记忆库管理器
    
    每个员工的记忆库结构：
    .agent/员工/{name}/记忆库/
    ├── work_log.md          # 工作日志（当月）
    ├── relations.md         # 人际关系
    ├── learnings.md         # 技能经验
    ├── index.json           # 索引文件
    └── 归档/
        ├── 2026-01/
        │   ├── work_log.md
        │   └── index.json
        └── 2025-12/
            └── ...
    """
    
    def __init__(self, employee_name: str, base_path: str = ".agent/员工"):
        """
        初始化记忆管理器
        
        Args:
            employee_name: 员工名称（如"大河"）
            base_path: 员工基础目录路径
        """
        self.employee_name = employee_name
        self.base_path = Path(base_path)
        self.memory_path = self.base_path / employee_name / "记忆库"
        
        # 确保目录存在
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保记忆库目录结构存在"""
        dirs = [
            self.memory_path,
            self.memory_path / "归档"
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
    
    # ==================== 读取操作 ====================
    
    def read_work_log(self, months: int = 2, include_archived: bool = False) -> List[MemoryEntry]:
        """
        读取工作日志
        
        Args:
            months: 读取最近几个月（默认2个月）
            include_archived: 是否包含归档文件
            
        Returns:
            记忆条目列表（按时间倒序）
        """
        entries = []
        
        # 1. 读取当前月
        current_file = self.memory_path / "work_log.md"
        if current_file.exists():
            entries.extend(self._parse_work_log(current_file.read_text(encoding='utf-8')))
        
        # 2. 如果需要，读取归档
        if include_archived and months > 1:
            archive_dir = self.memory_path / "归档"
            if archive_dir.exists():
                # 获取最近的归档月份
                archived_months = sorted([d for d in archive_dir.iterdir() if d.is_dir()], reverse=True)
                for month_dir in archived_months[:months-1]:
                    archive_file = month_dir / "work_log.md"
                    if archive_file.exists():
                        entries.extend(self._parse_work_log(archive_file.read_text(encoding='utf-8')))
        
        # 按时间倒序排序
        entries.sort(key=lambda x: x.timestamp, reverse=True)
        return entries
    
    def read_relations(self) -> List[MemoryEntry]:
        """读取人际关系记录"""
        file_path = self.memory_path / "relations.md"
        if not file_path.exists():
            return []
        return self._parse_simple_entries(file_path.read_text(encoding='utf-8'), MemoryType.RELATION)
    
    def read_learnings(self) -> List[MemoryEntry]:
        """读取技能经验记录"""
        file_path = self.memory_path / "learnings.md"
        if not file_path.exists():
            return []
        return self._parse_simple_entries(file_path.read_text(encoding='utf-8'), MemoryType.LEARNING)

    def read_chats(self, limit: int = 10) -> List[MemoryEntry]:
        """读取闲聊记录"""
        file_path = self.memory_path / "chat_log.md"
        if not file_path.exists():
            return []
        entries = self._parse_work_log(file_path.read_text(encoding='utf-8'))
        return entries[:limit]
    
    def get_memory_summary(self, max_entries: int = 20) -> str:
        """
        获取记忆摘要（用于加载到员工上下文）
        
        Args:
            max_entries: 最大条目数
            
        Returns:
            格式化的记忆摘要文本
        """
        summary_parts = []
        
        remaining = max(max_entries, 0)

        # 1. 最近工作（10条）
        work_limit = min(10, remaining)
        work_logs = self.read_work_log(months=2)[:work_limit]
        remaining -= work_limit
        if work_logs:
            summary_parts.append("## 近期工作")
            for entry in work_logs:
                summary_parts.append(f"- {entry.date}: {entry.content[:100]}")
        
        # 2. 关键关系（5条）
        relation_limit = min(5, remaining)
        relations = self.read_relations()[:relation_limit]
        remaining -= relation_limit
        if relations:
            summary_parts.append("\n## 关键关系")
            for entry in relations:
                summary_parts.append(f"- {entry.content[:100]}")
        
        # 3. 重要经验（5条）
        learning_limit = min(5, remaining)
        learnings = [e for e in self.read_learnings() if e.importance >= 4][:learning_limit]
        remaining -= learning_limit
        if learnings:
            summary_parts.append("\n## 重要经验")
            for entry in learnings:
                summary_parts.append(f"- {entry.content[:100]}")

        # 4. 近期闲聊（最多5条）
        chat_limit = min(5, remaining)
        chats = self.read_chats(limit=chat_limit)
        if chats:
            summary_parts.append("\n## 近期闲聊")
            for entry in chats:
                summary_parts.append(f"- {entry.date}: {entry.content[:100]}")
        
        return "\n".join(summary_parts) if summary_parts else "（暂无记忆）"
    
    # ==================== 写入操作 ====================
    
    def add_work_log(self, content: str, tags: Optional[List[str]] = None, importance: int = 3) -> bool:
        """
        添加工作日志
        
        Args:
            content: 日志内容（一句话描述）
            tags: 标签列表（可选）
            importance: 重要性（1-5）
            
        Returns:
            是否写入成功
        """
        if self._is_duplicate_entry(MemoryType.WORK_LOG, content, dedup_window=20):
            return True

        now = datetime.now()
        entry = MemoryEntry(
            timestamp=now.isoformat(),
            date=now.strftime("%Y-%m-%d"),
            content=content,
            source=self.employee_name,
            memory_type=MemoryType.WORK_LOG,
            tags=tags or [],
            importance=importance
        )
        
        return self._append_entry("work_log.md", entry)
    
    def add_relation(self, person: str, relationship: str, notes: str = "") -> bool:
        """
        添加人际关系记录
        
        Args:
            person: 人物名称
            relationship: 关系描述（如"同事"、"老板"）
            notes: 备注
        """
        content = f"**{person}**: {relationship}"
        if notes:
            content += f" - {notes}"
        
        if self._is_duplicate_entry(MemoryType.RELATION, content, dedup_window=20):
            return True

        now = datetime.now()
        entry = MemoryEntry(
            timestamp=now.isoformat(),
            date=now.strftime("%Y-%m-%d"),
            content=content,
            source=self.employee_name,
            memory_type=MemoryType.RELATION
        )
        
        return self._append_entry("relations.md", entry)
    
    def add_learning(self, content: str, category: str = "", importance: int = 3) -> bool:
        """
        添加技能经验
        
        Args:
            content: 经验内容
            category: 分类（如"Python"、"沟通技巧"）
            importance: 重要性（1-5）
        """
        if category:
            content = f"[{category}] {content}"
        
        if self._is_duplicate_entry(MemoryType.LEARNING, content, dedup_window=20):
            return True

        now = datetime.now()
        entry = MemoryEntry(
            timestamp=now.isoformat(),
            date=now.strftime("%Y-%m-%d"),
            content=content,
            source=self.employee_name,
            memory_type=MemoryType.LEARNING,
            importance=importance
        )
        
        return self._append_entry("learnings.md", entry)

    def add_chat(self, content: str, tags: Optional[List[str]] = None, importance: int = 2) -> bool:
        """
        添加闲聊记录（默认重要性更低）

        Args:
            content: 闲聊内容（一句话描述）
            tags: 标签列表（可选）
            importance: 重要性（1-5）

        Returns:
            是否写入成功
        """
        if self._is_duplicate_entry(MemoryType.CHAT, content, dedup_window=20):
            return True

        now = datetime.now()
        entry = MemoryEntry(
            timestamp=now.isoformat(),
            date=now.strftime("%Y-%m-%d"),
            content=content,
            source=self.employee_name,
            memory_type=MemoryType.CHAT,
            tags=tags or [],
            importance=importance
        )

        return self._append_entry("chat_log.md", entry)
    
    def _append_entry(self, filename: str, entry: MemoryEntry) -> bool:
        """追加条目到文件"""
        try:
            file_path = self.memory_path / filename

            if entry.memory_type == MemoryType.CHAT:
                self._prune_chat_entries(file_path, max_entries=10)
            
            # 构建条目文本
            entry_text = self._format_entry(entry)
            
            # 追加到文件
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(entry_text + "\n")
            
            # 更新索引
            self._update_index(entry)
            
            return True
        except Exception as e:
            print(f"[ERROR] 写入记忆失败: {e}")
            return False
    
    def _format_entry(self, entry: MemoryEntry) -> str:
        """格式化单条记忆为Markdown"""
        lines = [f"## {entry.date}"]
        
        # 元数据行
        meta = f"- {entry.content}"
        if entry.tags:
            meta += f" #{', #'.join(entry.tags)}"
        if entry.importance >= 4:
            meta += " ⭐"
        lines.append(meta)
        
        return "\n".join(lines)

    def _is_duplicate_entry(self, memory_type: MemoryType, content: str, dedup_window: int = 20) -> bool:
        """检查是否为重复记忆（基于内容归一化的近邻去重）"""
        recent_entries = self._get_recent_entries(memory_type, dedup_window)
        if not recent_entries:
            return False

        content_norm = self._normalize_content(content)
        if not content_norm:
            return False

        for entry in recent_entries:
            if self._normalize_content(entry.content) == content_norm:
                return True

        return False

    def _get_recent_entries(self, memory_type: MemoryType, limit: int) -> List[MemoryEntry]:
        """获取指定类型的最近条目"""
        handlers = {
            MemoryType.WORK_LOG: lambda: self.read_work_log(months=2)[:limit],
            MemoryType.RELATION: lambda: self.read_relations()[:limit],
            MemoryType.LEARNING: lambda: self.read_learnings()[:limit],
            MemoryType.CHAT: lambda: self.read_chats(limit=limit)
        }
        handler = handlers.get(memory_type)
        if handler is None:
            return []
        return handler()

    def _normalize_content(self, content: str) -> str:
        """内容归一化，用于去重比较"""
        if not content:
            return ""
        text = content.strip().lower()
        text = re.sub(r"#\w+", "", text)
        text = text.replace("⭐", "")
        text = re.sub(r"[^\w\u4e00-\u9fff]+", "", text)
        return text

    def _prune_chat_entries(self, file_path: Path, max_entries: int = 10):
        """闲聊超过上限时随机清理一条"""
        if not file_path.exists():
            return

        entries = self._parse_work_log(file_path.read_text(encoding='utf-8'))
        if len(entries) < max_entries:
            return

        remove_index = random.randrange(len(entries))
        remaining = [e for i, e in enumerate(entries) if i != remove_index]
        self._rewrite_entries(file_path, remaining)

    def _rewrite_entries(self, file_path: Path, entries: List[MemoryEntry]):
        """重写记忆文件"""
        header = f"# {file_path.stem.replace('_', ' ').title()}\n\n"
        chunks = [header]
        for entry in entries:
            chunks.append(self._format_entry(entry) + "\n")
        file_path.write_text("".join(chunks), encoding='utf-8')
    
    # ==================== 解析操作 ====================
    
    def _parse_work_log(self, content: str) -> List[MemoryEntry]:
        """解析工作日志Markdown为条目列表"""
        entries = []
        current_date = None
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # 日期行：## 2026-02-13
            date_match = re.match(r'##\s*(\d{4}-\d{2}-\d{2})', line)
            if date_match:
                current_date = date_match.group(1)
                continue
            
            # 内容行：- 完成了xxx #tag ⭐
            if line.startswith('- ') and current_date:
                content_text = line[2:].strip()
                
                # 提取标签
                tags = re.findall(r'#(\w+)', content_text)
                content_clean = re.sub(r'#\w+', '', content_text).strip()
                
                # 检查重要性标记
                importance = 4 if '⭐' in content_clean else 3
                content_clean = content_clean.replace('⭐', '').strip()
                
                entry = MemoryEntry(
                    timestamp=f"{current_date}T00:00:00",
                    date=current_date,
                    content=content_clean,
                    source=self.employee_name,
                    memory_type=MemoryType.WORK_LOG,
                    tags=tags,
                    importance=importance
                )
                entries.append(entry)
        
        return entries
    
    def _parse_simple_entries(self, content: str, memory_type: MemoryType) -> List[MemoryEntry]:
        """解析简单条目（人际关系、技能经验）"""
        entries = []
        current_date = None
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # 日期行
            date_match = re.match(r'##\s*(\d{4}-\d{2}-\d{2})', line)
            if date_match:
                current_date = date_match.group(1)
                continue
            
            # 内容行
            if line.startswith('- ') and current_date:
                entry = MemoryEntry(
                    timestamp=f"{current_date}T00:00:00",
                    date=current_date,
                    content=line[2:].strip(),
                    source=self.employee_name,
                    memory_type=memory_type
                )
                entries.append(entry)
        
        return entries
    
    # ==================== 归档操作 ====================
    
    def archive_current_month(self) -> bool:
        """
        归档当前月份的工作日志
        
        策略：每月1号执行，将上月的工作日志归档
        """
        try:
            now = datetime.now()
            # 上个月
            if now.month == 1:
                archive_year = now.year - 1
                archive_month = 12
            else:
                archive_year = now.year
                archive_month = now.month - 1
            
            archive_month_str = f"{archive_year}-{archive_month:02d}"
            archive_dir = self.memory_path / "归档" / archive_month_str
            archive_dir.mkdir(parents=True, exist_ok=True)
            
            # 归档 work_log.md
            work_log_file = self.memory_path / "work_log.md"
            if work_log_file.exists() and work_log_file.stat().st_size > 0:
                # 复制到归档目录
                shutil.copy2(work_log_file, archive_dir / "work_log.md")
                # 清空当前文件（保留标题）
                work_log_file.write_text("# 工作日志\n\n", encoding='utf-8')
                print(f"[INFO] 已归档 {self.employee_name} 的 {archive_month_str} 工作日志")
            
            return True
        except Exception as e:
            print(f"[ERROR] 归档失败: {e}")
            return False
    
    # ==================== 索引操作 ====================
    
    def _update_index(self, entry: MemoryEntry):
        """更新索引文件"""
        index_file = self.memory_path / "index.json"
        
        # 读取现有索引
        index = {}
        if index_file.exists():
            try:
                index = json.loads(index_file.read_text(encoding='utf-8'))
            except:
                index = {}
        
        # 更新统计
        month_key = entry.date[:7]  # 2026-02
        if "stats" not in index:
            index["stats"] = {}
        if month_key not in index["stats"]:
            index["stats"][month_key] = {"work_log": 0, "relation": 0, "learning": 0}
        
        index["stats"][month_key][entry.memory_type.value] += 1
        index["last_updated"] = datetime.now().isoformat()
        
        # 写入索引
        index_file.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding='utf-8')
    
    def get_stats(self) -> Dict[str, object]:
        """获取记忆统计信息"""
        index_file = self.memory_path / "index.json"
        if index_file.exists():
            try:
                return json.loads(index_file.read_text(encoding='utf-8'))
            except:
                pass
        return {}
    
    # ==================== 格式验证与修复 ====================
    
    def validate_and_fix(self) -> Tuple[bool, List[str]]:
        """
        验证并修复记忆库格式
        
        Returns:
            (是否全部正常, 错误信息列表)
        """
        errors = []
        
        for filename in ["work_log.md", "relations.md", "learnings.md", "chat_log.md"]:
            file_path = self.memory_path / filename
            if not file_path.exists():
                # 创建空文件
                file_path.write_text(f"# {filename.replace('.md', '').replace('_', ' ').title()}\n\n", encoding='utf-8')
                continue
            
            content = file_path.read_text(encoding='utf-8')
            
            # 检查是否有标题
            if not content.startswith("# "):
                # 修复：添加标题
                title = filename.replace('.md', '').replace('_', ' ').title()
                content = f"# {title}\n\n" + content
                file_path.write_text(content, encoding='utf-8')
                errors.append(f"{filename}: 缺少标题，已自动修复")
        
        return len(errors) == 0, errors


# ==================== 跨员工记忆访问 ====================

class CrossEmployeeMemory:
    """跨员工记忆访问（用于三核心员工互看）"""
    
    CORE_EMPLOYEES = ["大河", "海米", "困困"]
    
    def __init__(self, base_path: str = ".agent/员工"):
        self.base_path = Path(base_path)
    
    def read_employee_memory(self, employee_name: str, requester: str) -> Optional[str]:
        """
        读取其他员工的记忆（带权限检查）
        
        Args:
            employee_name: 被读取记忆的员工
            requester: 请求者（当前员工）
            
        Returns:
            记忆摘要，如果无权限返回None
        """
        # 权限检查：核心员工可以互看
        if requester not in self.CORE_EMPLOYEES:
            return None
        
        if employee_name not in self.CORE_EMPLOYEES:
            return None
        
        # 读取记忆
        manager = MemoryManager(employee_name, str(self.base_path))
        return manager.get_memory_summary()
    
    def list_core_memories(self, requester: str) -> Dict[str, str]:
        """列出所有核心员工的记忆摘要"""
        if requester not in self.CORE_EMPLOYEES:
            return {}
        
        result = {}
        for emp in self.CORE_EMPLOYEES:
            if emp != requester:  # 不列自己
                manager = MemoryManager(emp, str(self.base_path))
                result[emp] = manager.get_memory_summary(max_entries=10)
        return result


# ==================== 初始化模板 ====================

MEMORY_TEMPLATES = {
    "work_log.md": """# 工作日志

## 2026-02-13
- 入职正正公司 🎉

""",
    "relations.md": """# 人际关系

## 2026-02-13
- **正正**: 老板，我的直属领导

""",
    "learnings.md": """# 技能经验

## 2026-02-13
    - [入职] 加入正正公司，开始记录工作经验

    """,
    "chat_log.md": """# 闲聊记录

## 2026-02-13
- 和正正闲聊，了解偏好与沟通风格

"""
}


def initialize_employee_memory(employee_name: str, base_path: str = ".agent/员工") -> bool:
    """
    初始化员工记忆库（用于新员工入职）
    
    Args:
        employee_name: 员工名称
        base_path: 基础路径
        
    Returns:
        是否初始化成功
    """
    try:
        memory_path = Path(base_path) / employee_name / "记忆库"
        memory_path.mkdir(parents=True, exist_ok=True)
        
        # 创建三档案
        for filename, content in MEMORY_TEMPLATES.items():
            file_path = memory_path / filename
            if not file_path.exists():
                file_path.write_text(content, encoding='utf-8')
        
        # 创建归档目录
        (memory_path / "归档").mkdir(exist_ok=True)
        
        print(f"[INFO] 已为 {employee_name} 初始化记忆库")
        return True
    except Exception as e:
        print(f"[ERROR] 初始化记忆库失败: {e}")
        return False


if __name__ == "__main__":
    # 测试代码
    print("记忆库系统核心模块")
    print("=" * 50)
    
    # 初始化测试员工
    initialize_employee_memory("测试员工")
    
    # 测试写入
    manager = MemoryManager("测试员工")
    manager.add_work_log("完成了记忆库系统核心模块开发", tags=["核心", "开发"], importance=5)
    manager.add_relation("大河", "HR总监", "负责招聘和员工管理")
    manager.add_learning("Python pathlib 模块比 os.path 更好用", "Python", importance=4)
    
    # 测试读取
    print("\n记忆摘要：")
    print(manager.get_memory_summary())
    
    # 验证格式
    is_valid, errors = manager.validate_and_fix()
    if errors:
        print(f"\n修复项: {errors}")
