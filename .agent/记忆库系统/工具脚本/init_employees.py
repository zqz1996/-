#!/usr/bin/env python3
"""
初始化现有员工记忆库
为大河、海米、困困三位核心员工创建记忆库结构
"""

import sys
from pathlib import Path

# 添加核心模块路径
sys.path.insert(0, str(Path(__file__).parent.parent / "核心模块"))

from memory_manager import initialize_employee_memory

def main():
    """初始化三核心员工的记忆库"""
    employees = ["大河", "海米", "困困"]
    
    print("="*60)
    print("正正公司员工记忆库初始化")
    print("="*60)
    print()
    
    for emp in employees:
        print(f"正在初始化 {emp} 的记忆库...")
        success = initialize_employee_memory(emp)
        if success:
            print(f"✅ {emp}: 初始化完成")
        else:
            print(f"❌ {emp}: 初始化失败")
        print()
    
    print("="*60)
    print("✅ 所有员工记忆库初始化完成！")
    print("="*60)

if __name__ == "__main__":
    main()
