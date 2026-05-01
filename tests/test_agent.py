"""
AgentMessage 单元测试

测试消息格式的创建、序列化和反序列化。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from agent import AgentMessage


class TestAgentMessage:
    """AgentMessage 测试类"""
    
    def test_create_message(self):
        """测试创建消息"""
        msg = AgentMessage(
            sender="agent://localhost:8765/alice",
            receiver="agent://localhost:8766/bob",
            msg_type="request",
            payload={"intent": "greet", "message": "Hello!"}
        )
        
        assert msg.sender == "agent://localhost:8765/alice"
        assert msg.receiver == "agent://localhost:8766/bob"
        assert msg.type == "request"
        assert msg.payload == {"intent": "greet", "message": "Hello!"}
        assert msg.id is not None
        assert msg.timestamp is not None
    
    def test_message_to_dict(self):
        """测试消息转字典"""
        msg = AgentMessage(
            sender="agent://localhost:8765/alice",
            receiver="agent://localhost:8766/bob",
            msg_type="request",
            payload={"intent": "test"}
        )
        
        d = msg.to_dict()
        
        assert d["sender"] == "agent://localhost:8765/alice"
        assert d["receiver"] == "agent://localhost:8766/bob"
        assert d["type"] == "request"
        assert d["payload"] == {"intent": "test"}
        assert "id" in d
        assert "timestamp" in d
    
    def test_message_from_dict(self):
        """测试从字典创建消息"""
        data = {
            "id": "test-123",
            "sender": "agent://localhost:8765/alice",
            "receiver": "agent://localhost:8766/bob",
            "type": "response",
            "payload": {"result": "ok"},
            "timestamp": "2026-05-01T12:00:00"
        }
        
        msg = AgentMessage.from_dict(data)
        
        assert msg.id == "test-123"
        assert msg.sender == "agent://localhost:8765/alice"
        assert msg.receiver == "agent://localhost:8766/bob"
        assert msg.type == "response"
        assert msg.payload == {"result": "ok"}
    
    def test_message_roundtrip(self):
        """测试消息序列化/反序列化往返"""
        original = AgentMessage(
            sender="agent://localhost:8765/alice",
            receiver="agent://localhost:8766/bob",
            msg_type="request",
            payload={"intent": "test", "data": [1, 2, 3]}
        )
        
        # 序列化
        d = original.to_dict()
        
        # 反序列化
        restored = AgentMessage.from_dict(d)
        
        # 验证
        assert restored.sender == original.sender
        assert restored.receiver == original.receiver
        assert restored.type == original.type
        assert restored.payload == original.payload
    
    def test_message_repr(self):
        """测试消息字符串表示"""
        msg = AgentMessage(
            sender="alice",
            receiver="bob",
            msg_type="request",
            payload={"intent": "test"}
        )
        
        repr_str = repr(msg)
        assert "request" in repr_str
        assert "alice" in repr_str
        assert "bob" in repr_str


def run_tests():
    """运行所有测试"""
    test = TestAgentMessage()
    
    print("运行 AgentMessage 测试...")
    print("-" * 40)
    
    tests = [
        test.test_create_message,
        test.test_message_to_dict,
        test.test_message_from_dict,
        test.test_message_roundtrip,
        test.test_message_repr,
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
