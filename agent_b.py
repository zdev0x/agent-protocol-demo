#!/usr/bin/env python3
"""
Agent B - 响应方
演示：接收并处理约饭请求
"""

import asyncio
import json
import websockets
from agent import Agent


async def register_with_registry(agent: Agent, registry_uri: str = "ws://localhost:8766"):
    """向 Registry 注册自己"""
    async with websockets.connect(registry_uri) as ws:
        await ws.send(json.dumps({
            "action": "register",
            "uri": agent.uri,
            "name": agent.name,
            "capabilities": agent.capabilities
        }))
        response = json.loads(await ws.recv())
        print(f"📡 注册结果: {response['message']}")


async def handle_request(msg):
    """处理收到的消息"""
    payload = msg.payload
    intent = payload.get("intent")
    
    print(f"\n💬 [{msg.receiver}] 收到消息:")
    print(f"   类型: {msg.type}")
    print(f"   意图: {intent}")
    print(f"   内容: {payload.get('message')}")
    
    if intent == "book_meeting":
        # 约饭请求
        proposed_time = payload.get("proposed_time")
        print(f"\n🤔 思考中... (对方提议: {proposed_time})")
        await asyncio.sleep(1)  # 模拟思考
        
        # 同意并推荐地点
        response = {
            "accepted": True,
            "message": "好的，我有空！",
            "confirmed_time": proposed_time,
            "location": "上海人民广场海底捞 🍲"
        }
        print(f"   → 回复: 同意，推荐地点")
        return response
    
    elif intent == "confirm":
        # 确认
        print(f"\n👍 收到确认，准备赴约！")
        return {
            "message": "好的，明天见！",
            "status": "confirmed"
        }
    
    return {"message": "收到"}


async def main():
    # 1. 创建 Agent B
    agent = Agent(
        name="bob",
        port=8766,
        capabilities=["booking", "scheduling"]
    )
    
    # 2. 注册消息处理器
    agent.on_message(handle_request)
    
    # 3. 注册到 Registry
    await register_with_registry(agent)
    
    # 4. 启动服务（等待 Agent A 的消息）
    print("\n🚀 Agent B 已就绪，等待 Agent A 的消息...")
    print("="*50)
    
    await agent.start()
    
    try:
        await asyncio.Future()  # 保持运行
    except KeyboardInterrupt:
        await agent.stop()


if __name__ == "__main__":
    asyncio.run(main())
