#!/usr/bin/env python3
"""
ACP v0.1 Demo - 4 个核心动作

演示 Agent 通讯协议的 4 个核心动作：
1. register    - Agent 注册
2. discover    - 能力发现
3. send_task   - 发送任务
4. get_status  - 查询状态

场景：买家 Agent 通过 Registry 找到卖家 Agent，发送购物任务
"""

import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))


async def main():
    print("=" * 60)
    print("🤖 ACP v0.1 Demo - 4 个核心动作")
    print("=" * 60)
    print()
    print("ACP (Agent Communication Protocol) 轻量级协议演示")
    print()
    print("核心动作:")
    print("  1. register    - Agent 注册")
    print("  2. discover    - 能力发现")
    print("  3. send_task   - 发送任务")
    print("  4. get_status  - 查询状态")
    print()
    print("=" * 60)
    print()

    # 1. 启动 Registry
    from registry import AgentRegistry
    registry = AgentRegistry(port=8767)
    await registry.start()
    await asyncio.sleep(0.5)

    # 2. 启动卖家 Agent
    from agent import Agent

    async def handle_task(msg):
        """处理任务请求"""
        payload = msg.payload
        action = payload.get("action")

        print(f"\n💬 [{msg.receiver}] 收到请求:")
        print(f"   动作: {action}")

        if action == "send_task":
            task = payload.get("task", {})
            task_id = task.get("task_id")
            task_type = task.get("type")
            task_input = task.get("input", {})

            print(f"   任务 ID: {task_id}")
            print(f"   任务类型: {task_type}")
            print(f"   任务输入: {json.dumps(task_input, ensure_ascii=False)}")

            # 模拟任务执行
            await asyncio.sleep(1)

            # 返回任务结果
            return {
                "action": "send_task_response",
                "task_id": task_id,
                "accepted": True,
                "status": "completed",
                "result": {
                    "product": "MacBook Pro 14 M3 Pro",
                    "price": 14999,
                    "currency": "CNY",
                    "seller": "Apple Store 官方旗舰店",
                    "order_id": "ORD-20260501-001",
                    "estimated_delivery": "2026-05-03"
                }
            }

        elif action == "get_status":
            task_id = payload.get("task_id")
            print(f"   查询任务: {task_id}")

            return {
                "action": "get_status_response",
                "task_id": task_id,
                "state": "completed",
                "result": {
                    "product": "MacBook Pro 14 M3 Pro",
                    "price": 14999,
                    "order_id": "ORD-20260501-001"
                }
            }

        return {"error": "unknown_action"}

    # 创建卖家 Agent
    seller = Agent(name="seller", port=8766, capabilities=["shopping", "order"])
    seller.on_message(handle_task)

    # 注册到 Registry
    import websockets
    async with websockets.connect("ws://localhost:8767") as ws:
        await ws.send(json.dumps({
            "action": "register",
            "uri": seller.uri,
            "name": seller.name,
            "capabilities": seller.capabilities
        }))
        await ws.recv()
    await seller.start()
    await asyncio.sleep(0.5)

    # 3. 启动买家 Agent
    buyer = Agent(name="buyer", port=8765, capabilities=["shopping"])
    await buyer.start()
    await asyncio.sleep(0.5)

    # ========================================
    # ACP v0.1 核心动作演示
    # ========================================

    print("\n" + "=" * 60)
    print("📋 ACP v0.1 核心动作演示")
    print("=" * 60)

    # 动作 1: register (已在上面完成)
    print("\n" + "-" * 40)
    print("1️⃣  register - Agent 注册")
    print("-" * 40)
    print(f"✅ 卖家 Agent 已注册到 Registry")
    print(f"   URI: {seller.uri}")
    print(f"   能力: {seller.capabilities}")

    # 动作 2: discover
    print("\n" + "-" * 40)
    print("2️⃣  discover - 能力发现")
    print("-" * 40)

    async with websockets.connect("ws://localhost:8767") as ws:
        await ws.send(json.dumps({
            "action": "find",
            "capability": "shopping"
        }))
        result = json.loads(await ws.recv())
        discovered_agents = result.get("agents", [])

    print(f"🔍 搜索能力 [shopping]: 找到 {len(discovered_agents)} 个 Agent")
    for agent_uri in discovered_agents:
        print(f"   - {agent_uri}")

    # 动作 3: send_task
    print("\n" + "-" * 40)
    print("3️⃣  send_task - 发送任务")
    print("-" * 40)

    task = {
        "task_id": "task-20260501-001",
        "type": "shopping.order",
        "input": {
            "product": "MacBook Pro 14 M3 Pro",
            "quantity": 1,
            "shipping_address": "上海市黄浦区南京东路 100 号"
        }
    }

    print(f"📤 发送任务:")
    print(f"   任务 ID: {task['task_id']}")
    print(f"   任务类型: {task['type']}")
    print(f"   商品: {task['input']['product']}")

    response = await buyer.send_to(
        discovered_agents[0],
        {"action": "send_task", "task": task}
    )

    if response.get("accepted"):
        print(f"\n✅ 任务已接受")
        print(f"   订单号: {response['result']['order_id']}")
        print(f"   价格: ¥{response['result']['price']}")
        print(f"   预计送达: {response['result']['estimated_delivery']}")

    # 动作 4: get_status
    print("\n" + "-" * 40)
    print("4️⃣  get_status - 查询状态")
    print("-" * 40)

    print(f"📥 查询任务状态: {task['task_id']}")

    status_response = await buyer.send_to(
        discovered_agents[0],
        {"action": "get_status", "task_id": task["task_id"]}
    )

    print(f"   任务状态: {status_response.get('state', 'unknown')}")
    if "result" in status_response:
        print(f"   结果: {json.dumps(status_response['result'], ensure_ascii=False)}")

    # 完成
    print("\n" + "=" * 60)
    print("🎉 ACP v0.1 Demo 完成！")
    print("=" * 60)
    print()
    print("总结 - ACP v0.1 4 个核心动作:")
    print("  1. ✅ register    - Agent 注册到 Registry")
    print("  2. ✅ discover    - 根据能力发现 Agent")
    print("  3. ✅ send_task   - 向 Agent 发送任务")
    print("  4. ✅ get_status  - 查询任务执行状态")
    print()
    print("这就是 ACP 的核心 - 简单、可实现、低依赖 🚀")
    print()

    # 关闭
    await buyer.stop()
    await seller.stop()
    await registry.stop()


if __name__ == "__main__":
    asyncio.run(main())
