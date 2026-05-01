#!/usr/bin/env python3
"""
Agent A - 发起方
演示：向 Agent B 发起约饭请求
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


async def main():
    # 1. 创建 Agent A
    agent = Agent(
        name="alice",
        port=8765,
        capabilities=["scheduling", "negotiation"]
    )
    
    # 2. 注册到 Registry
    await register_with_registry(agent)
    
    # 3. 等一下让 Agent B 也启动
    print("\n⏳ 等待 2 秒让 Agent B 启动...")
    await asyncio.sleep(2)
    
    # 4. 发现 Agent B
    print("\n🔍 通过 Registry 搜索 Agent B...")
    async with websockets.connect("ws://localhost:8766") as ws:
        await ws.send(json.dumps({
            "action": "find",
            "capability": "booking"
        }))
        result = json.loads(await ws.recv())
        target_uri = result["agents"][0]
        print(f"   找到目标: {target_uri}")
    
    # 5. 发起约饭对话
    print("\n" + "="*50)
    print("🍽️  开始约饭对话")
    print("="*50)
    
    response = await agent.send_to(target_uri, {
        "intent": "book_meeting",
        "message": "你好，我想约明天下午吃饭，有空吗？",
        "proposed_time": "明天 14:00"
    })
    
    # 6. 处理响应
    if response.get("accepted"):
        print(f"\n✅ 约饭成功！")
        print(f"   时间: {response.get('confirmed_time')}")
        print(f"   地点: {response.get('location')}")
        
        # 确认
        await agent.send_to(target_uri, {
            "intent": "confirm",
            "message": "收到，明天见！"
        }, msg_type="confirm")
    else:
        print(f"\n❌ 约饭失败: {response.get('message')}")
    
    print("\n" + "="*50)
    print("🎉 Demo 完成！")
    print("="*50)


if __name__ == "__main__":
    asyncio.run(main())
