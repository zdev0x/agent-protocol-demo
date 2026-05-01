#!/usr/bin/env python3
"""
测试运行器

运行所有单元测试。

使用方法:
    python run_tests.py
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from tests.test_agent import run_tests as run_agent_tests
from tests.test_registry import run_tests as run_registry_tests


def main():
    """运行所有测试"""
    print("=" * 60)
    print("🧪 Agent Protocol 测试套件")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # 运行 AgentMessage 测试
    print("📦 AgentMessage 测试")
    print("-" * 60)
    if not run_agent_tests():
        all_passed = False
    print()
    
    # 运行 AgentRegistry 测试
    print("📦 AgentRegistry 测试")
    print("-" * 60)
    if not run_registry_tests():
        all_passed = False
    print()
    
    # 汇总结果
    print("=" * 60)
    if all_passed:
        print("✅ 所有测试通过！")
    else:
        print("❌ 部分测试失败")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
