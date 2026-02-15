#!/usr/bin/env python3
"""
记忆库自动化维护脚本
Memory Maintenance Automation Scripts

功能：
- 每月自动归档
- 健康检查
- 备份
- 统计报告

执行方式：
- 手动: python memory_maintenance.py --archive
- 定时: 添加到系统cron（每月1号执行）

作者：正正公司技术团队
版本：1.0.0
"""

import os
import sys
import json
import shutil
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple, Any

# 添加核心模块到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "核心模块"))
from memory_manager import MemoryManager, initialize_employee_memory, CrossEmployeeMemory


class MemoryMaintenance:
    """记忆库维护器"""
    
    def __init__(self, base_path: str = ".agent/员工"):
        self.base_path = Path(base_path)
        self.employees = self._get_all_employees()
    
    def _get_all_employees(self) -> List[str]:
        """获取所有员工列表"""
        employees = []
        if self.base_path.exists():
            for emp_dir in self.base_path.iterdir():
                if emp_dir.is_dir() and not emp_dir.name.startswith('.'):
                    # 检查是否有记忆库
                    if (emp_dir / "记忆库").exists():
                        employees.append(emp_dir.name)
        return employees
    
    # ==================== 归档功能 ====================
    
    def archive_all(self, dry_run: bool = False) -> Dict[str, bool]:
        """
        归档所有员工的记忆库
        
        Args:
            dry_run: 如果为True，只显示将要执行的操作，不实际执行
            
        Returns:
            每个员工的归档结果
        """
        results = {}
        
        print(f"\n{'='*60}")
        print(f"记忆库归档任务")
        print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"员工数量: {len(self.employees)}")
        print(f"{'='*60}\n")
        
        for emp in self.employees:
            if dry_run:
                print(f"[DRY-RUN] 将归档 {emp} 的当前月工作日志")
                results[emp] = True
            else:
                manager = MemoryManager(emp, str(self.base_path))
                success = manager.archive_current_month()
                results[emp] = success
                status = "✅ 成功" if success else "❌ 失败"
                print(f"{status}: {emp}")
        
        return results
    
    # ==================== 健康检查 ====================
    
    def health_check(self) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        执行健康检查
        
        检查项：
        1. 文件格式是否正确
        2. 是否有损坏的索引
        3. 文件大小是否合理（不超过10MB）
        4. 是否有空文件
        
        Returns:
            (是否全部健康, 问题列表)
        """
        issues = []
        all_healthy = True
        
        print(f"\n{'='*60}")
        print(f"记忆库健康检查")
        print(f"{'='*60}\n")
        
        for emp in self.employees:
            print(f"检查 {emp}...")
            memory_path = self.base_path / emp / "记忆库"
            
            # 检查各文件
            for filename in ["work_log.md", "relations.md", "learnings.md", "chat_log.md"]:
                file_path = memory_path / filename
                
                if not file_path.exists():
                    issues.append({
                        "employee": emp,
                        "file": filename,
                        "issue": "文件不存在",
                        "severity": "high"
                    })
                    all_healthy = False
                    continue
                
                # 检查文件大小
                size = file_path.stat().st_size
                if size > 10 * 1024 * 1024:  # 10MB
                    issues.append({
                        "employee": emp,
                        "file": filename,
                        "issue": f"文件过大 ({size / 1024 / 1024:.1f} MB)，需要归档",
                        "severity": "medium"
                    })
                
                # 检查是否为空（除了标题）
                content = file_path.read_text(encoding='utf-8')
                lines = [l for l in content.split('\n') if l.strip() and not l.startswith('#')]
                if len(lines) < 2:
                    issues.append({
                        "employee": emp,
                        "file": filename,
                        "issue": "文件内容过少，建议添加更多记录",
                        "severity": "low"
                    })
            
            # 验证并尝试修复
            manager = MemoryManager(emp, str(self.base_path))
            _is_valid, errors = manager.validate_and_fix()
            if errors:
                for error in errors:
                    issues.append({
                        "employee": emp,
                        "file": "format",
                        "issue": error,
                        "severity": "low",
                        "auto_fixed": True
                    })
        
        # 打印报告
        print(f"\n{'='*60}")
        print(f"检查结果: {'✅ 全部健康' if all_healthy else '⚠️ 发现问题'}")
        print(f"问题数量: {len(issues)}")
        print(f"{'='*60}\n")
        
        if issues:
            for issue in issues:
                severity_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(issue['severity'], "⚪")
                fixed_tag = " [已自动修复]" if issue.get('auto_fixed') else ""
                print(f"{severity_icon} [{issue['employee']}] {issue['file']}: {issue['issue']}{fixed_tag}")
        
        return all_healthy, issues
    
    # ==================== 备份功能 ====================
    
    def backup_all(self, backup_dir: str = ".agent/记忆库系统/备份") -> bool:
        """
        备份所有员工记忆库
        
        Args:
            backup_dir: 备份目录
            
        Returns:
            是否备份成功
        """
        backup_path = Path(backup_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"memory_backup_{timestamp}"
        full_backup_path = backup_path / backup_name
        
        print(f"\n{'='*60}")
        print(f"记忆库备份")
        print(f"备份路径: {full_backup_path}")
        print(f"{'='*60}\n")
        
        try:
            full_backup_path.mkdir(parents=True, exist_ok=True)
            
            for emp in self.employees:
                source = self.base_path / emp / "记忆库"
                dest = full_backup_path / emp
                
                if source.exists():
                    shutil.copytree(source, dest, dirs_exist_ok=True)
                    print(f"✅ 已备份: {emp}")
            
            # 创建备份信息文件
            backup_info = {
                "timestamp": timestamp,
                "employees": self.employees,
                "total_size_mb": sum(
                    f.stat().st_size for f in full_backup_path.rglob('*') if f.is_file()
                ) / 1024 / 1024
            }
            (full_backup_path / "backup_info.json").write_text(
                json.dumps(backup_info, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
            
            print(f"\n{'='*60}")
            print(f"✅ 备份完成: {full_backup_path}")
            print(f"{'='*60}\n")
            return True
            
        except Exception as e:
            print(f"\n❌ 备份失败: {e}")
            return False
    
    # ==================== 统计报告 ====================
    
    def generate_report(self) -> str:
        """
        生成记忆库统计报告
        
        Returns:
            Markdown格式的报告
        """
        lines = [
            "# 正正公司员工记忆库统计报告",
            f"",
            f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"员工数量: {len(self.employees)}",
            f"",
            "## 员工记忆概况",
            ""
        ]
        
        for emp in self.employees:
            manager = MemoryManager(emp, str(self.base_path))
            stats = manager.get_stats()
            stats_map: Dict[str, Dict[str, int]] = {}
            if isinstance(stats, dict):
                raw_stats = stats.get("stats")
                if isinstance(raw_stats, dict):
                    stats_map = raw_stats
            
            lines.append(f"### {emp}")
            lines.append("")
            
            if stats_map:
                for month, counts in sorted(stats_map.items(), reverse=True)[:3]:
                    total = sum(counts.values())
                    lines.append(f"- **{month}**: {total} 条记录")
                    for mem_type, count in counts.items():
                        if count > 0:
                            lines.append(f"  - {mem_type}: {count}")
            else:
                lines.append("- （暂无统计数据）")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def save_report(self, output_dir: str = ".agent/记忆库系统/报告") -> str:
        """保存统计报告到文件"""
        report_path = Path(output_dir)
        report_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"memory_report_{timestamp}.md"
        file_path = report_path / filename
        
        report = self.generate_report()
        file_path.write_text(report, encoding='utf-8')
        
        print(f"\n✅ 报告已保存: {file_path}")
        return str(file_path)


# ==================== 命令行接口 ====================

def main():
    parser = argparse.ArgumentParser(
        description="正正公司员工记忆库自动化维护工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 执行归档（实际执行）
  python memory_maintenance.py --archive
  
  # 试运行（不实际执行）
  python memory_maintenance.py --archive --dry-run
  
  # 健康检查
  python memory_maintenance.py --health
  
  # 生成报告
  python memory_maintenance.py --report
  
  # 备份
  python memory_maintenance.py --backup
  
  # 全部执行
  python memory_maintenance.py --all
        """
    )
    
    parser.add_argument("--archive", action="store_true", help="归档上月的记忆")
    parser.add_argument("--dry-run", action="store_true", help="试运行模式（只显示不执行）")
    parser.add_argument("--health", action="store_true", help="执行健康检查")
    parser.add_argument("--backup", action="store_true", help="备份所有记忆库")
    parser.add_argument("--report", action="store_true", help="生成统计报告")
    parser.add_argument("--all", action="store_true", help="执行全部维护任务")
    parser.add_argument("--base-path", default=".agent/员工", help="员工基础目录（默认: .agent/员工）")
    
    args = parser.parse_args()
    
    # 如果没有指定任何操作，显示帮助
    if not any([args.archive, args.health, args.backup, args.report, args.all]):
        parser.print_help()
        return
    
    # 创建维护器
    maintainer = MemoryMaintenance(args.base_path)
    
    # 执行操作
    if args.all or args.archive:
        maintainer.archive_all(dry_run=args.dry_run)
    
    if args.all or args.health:
        maintainer.health_check()
    
    if args.all or args.backup:
        maintainer.backup_all()
    
    if args.all or args.report:
        maintainer.save_report()
    
    print("\n✅ 维护任务完成！\n")


if __name__ == "__main__":
    main()
