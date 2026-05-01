#!/usr/bin/env python3
"""
一键运行 Demo
启动 Registry + Agent A + Agent B
"""

import asyncio
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))


async def main():
    print("="*60)
    print("🚀 Agent 通讯协议 Demo")
    print("="*60)
    print()
    print("这个 Demo 演示了两个 Agent 通过协议进行约饭对话:")
    print()
    print("  Agent A (Alice) → Agent B (Bob)")
    print("       ↓               ↓")
    print("  发起约饭请求    响应并确认")
    print()
    print("="*60)
    print()
    
    # 1. 启动 Registry
    from registry import AgentRegistry
    registry = AgentRegistry()
    await registry.start()
    
    await asyncio.sleep(1)
    
    # 2. 启动 Agent B（响应方）
    from agent import Agent
    
    async def handle_request(msg):
        payload = msg.payload
        intent = payload.get("intent")
        
        print(f"\n💬 [{msg.receiver}] 收到消息:")
        print(f"   类型: {msg.type}")
        print(f"   意图: {intent}")
        print(f"   内容: {payload.get('message')}")
        
        if intent == "book_meeting":
            proposed_time = payload.get("proposed_time")
            print(f"\n🤔 思考中... (对方提议: {proposed_time})")
            await asyncio.sleep(1)
            
            response = {
                "accepted": True,
                "message": "好的，我有空！",
                "confirmed_time": proposed_time,
                "location": "上海人民广场海底捞 🍲"
            }
            print(f"   → 回复: 同意，推荐地点")
            return response
        
        elif intent == "confirm":
            print(f"\n👍 收到确认，准备赴约！")
            return {
                "message": "好的，明天见！",
                "status": "confirmed"
            }
        
        return {"message": "收到"}
    
    agent_b = Agent(
        name="bob",
        port=8766,
        capabilities=["booking", "scheduling"]
    )
    agent_b.on_message(handle_request)
    
    # 注册到 Registry
    import websockets
    async with websockets.connect("ws://localhost:8766") as ws:
        await ws.send(json.dumps({
            "action": "register",
            "uri": agent_b.uri,
            "name": agent_b.name,
            "capabilities": agent_b.capabilities
        }))
        await ws.recv()
    
    await agent_b.start()
    await asyncio.sleep(1)
    
    # 3. 启动 Agent A（发起方）
    agent_a = Agent(
        name="alice",
        port=8765,
        capabilities=["scheduling", "negotiation"]
    )
    
    # 注册到 Registry
    async with websockets.connect("ws://localhost:8766") as ws:
        await ws.send(json.dumps({
            "action": "register",
            "uri": agent_a.uri,
            "name": agent_a.name,
            "capabilities": agent_a.capabilities
        }))
        await ws.recv()
    
    await agent_a.start()
    await asyncio.sleep(1)
    
    # 4. Agent A 发起约饭
    print("\n" + "="*60)
    print("🍽️  Alice 向 Bob 发起约饭请求")
    print("="*60)
    
    # 找到 Bob
    async with websockets.connect("ws://localhost:8766") as ws:
        await ws.send(json.dumps({
            "action": "find",
            "capability": "booking"
        }))
        result = json.loads(await ws.recv())
        target_uri = result["agents"][0]
        print(f"🔍 通过 Registry 找到: {target_uri}")
    
    # 发送约饭请求
    response = await agent_a.send_to(target_uri, {
        "intent": "book_meeting",
        "message": "你好，我想约明天下午吃饭，有空吗？",
        "proposed_time": "明天 14:00"
    })
    
    if response.get("accepted"):
        print(f"\n✅ 约饭成功！")
        print(f"   时间: {response.get('confirmed_time')}")
        print(f"   地点: {response.get('location')}")
        
        # 发送确认
        await agent_a.send_to(target_uri, {
            "intent": "confirm",
            "message": "收到，明天见！"
        }, msg_type="confirm")
    
    # 5. 完成
    print("\n" + "="*60)
    print("🎉 Demo 完成！")
    print("="*60)
    print()
    print("总结:")
    print("  1. Agent 通过 Registry 发现彼此")
    print("  2. Agent 之间通过 WebSocket 通讯")
    print("  3. 消息格式标准化 (AgentMessage)")
    print("  4. 支持异步任务和确认机制")
    print()
    print("下一步:")
    print("  - 实现更多能力搜索")
    print("  - 添加消息加密")
    print("  - 分布式部署")
    print()
    
    # 关闭所有
    await agent_a.stop()
    await agent_b.stop()
    await registry.stop()


if __name__ == "__main__":
    import json
    asyncio.run(main())
