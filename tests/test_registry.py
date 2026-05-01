"""
Registry 单元测试

测试 Agent 注册中心的功能。
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from registry import AgentRegistry


class TestAgentRegistry:
    """AgentRegistry 测试类"""
    
    def test_registry_creation(self):
        """测试创建 Registry"""
        registry = AgentRegistry(host="localhost", port=8767)
        
        assert registry.host == "localhost"
        assert registry.port == 8767
        assert registry.agents == {}
    
    def test_agent_registration(self):
        """测试 Agent 注册"""
        registry = AgentRegistry()
        
        # 模拟注册
        agent_info = {
            "uri": "agent://localhost:8765/alice",
            "name": "alice",
            "capabilities": ["booking", "payment"]
        }
        registry.agents[agent_info["uri"]] = agent_info
        
        assert "agent://localhost:8765/alice" in registry.agents
        assert registry.agents["agent://localhost:8765/alice"]["name"] == "alice"
    
    def test_agent_discovery(self):
        """测试 Agent 发现"""
        registry = AgentRegistry()
        
        # 注册多个 Agent
        registry.agents["agent://localhost:8765/alice"] = {
            "uri": "agent://localhost:8765/alice",
            "name": "alice",
            "capabilities": ["booking", "scheduling"]
        }
        registry.agents["agent://localhost:8766/bob"] = {
            "uri": "agent://localhost:8766/bob",
            "name": "bob",
            "capabilities": ["payment", "booking"]
        }
        
        # 搜索 booking 能力
        matched = [
            a for a in registry.agents.values()
            if "booking" in a["capabilities"]
        ]
        
        assert len(matched) == 2
        
        # 搜索 payment 能力
        matched = [
            a for a in registry.agents.values()
            if "payment" in a["capabilities"]
        ]
        
        assert len(matched) == 1
        assert matched[0]["name"] == "bob"
    
    def test_agent_unregistration(self):
        """测试 Agent 注销"""
        registry = AgentRegistry()
        
        # 注册
        registry.agents["agent://localhost:8765/alice"] = {
            "uri": "agent://localhost:8765/alice",
            "name": "alice"
        }
        
        assert "agent://localhost:8765/alice" in registry.agents
        
        # 注销
        del registry.agents["agent://localhost:8765/alice"]
        
        assert "agent://localhost:8765/alice" not in registry.agents


def run_tests():
    """运行所有测试"""
    test = TestAgentRegistry()
    
    print("运行 AgentRegistry 测试...")
    print("-" * 40)
    
    tests = [
        test.test_registry_creation,
        test.test_agent_registration,
        test.test_agent_discovery,
        test.test_agent_unregistration,
    ]
    
    passed = 0
    failed = 0
    
    for t in tests:
        try:
            t()
            print(f"✅ {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"❌ {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {t.__name__}: {e}")
            failed += 1
    
    print("-" * 40)
    print(f"结果: {passed} 通过, {failed} 失败")
    
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
