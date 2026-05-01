#!/usr/bin/env python3
"""
Agent 通讯协议 Demo - 购物场景
买家 Agent 自动搜索、比价、下单
"""

import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))


async def main():
    print("=" * 60)
    print("🛒 Agent 购物协议 Demo")
    print("=" * 60)
    print()
    print("场景：买家 Agent 自动搜索商品、比价、下单")
    print()
    print("  👤 用户: \"我想买一台 MacBook Pro\"")
    print("     ↓")
    print("  🤖 买家 Agent → Hub → 找到多个卖家")
    print("     ↓")
    print("  🤖 买家 Agent: 比较价格、评价、库存")
    print("     ↓")
    print("  🤖 买家 Agent: 自动下单")
    print("     ↓")
    print("  📦 订单确认，等待发货")
    print()
    print("=" * 60)
    print()

    # 1. 启动 Registry (端口 8767)
    from registry import AgentRegistry
    registry = AgentRegistry(port=8767)
    await registry.start()
    await asyncio.sleep(0.5)

    # 2. 启动卖家 Agent（多个店铺）
    from agent import Agent

    # 卖家 A - Apple Store
    async def handle_seller_a(msg):
        payload = msg.payload
        intent = payload.get("intent")

        print(f"\n💬 [{msg.receiver}] 收到消息:")
        print(f"   意图: {intent}")

        if intent == "product.search":
            product = payload.get("product", "")
            print(f"   搜索商品: {product}")
            await asyncio.sleep(0.5)

            return {
                "intent": "product.search.result",
                "products": [
                    {
                        "id": "MBP-001",
                        "name": "MacBook Pro 14 M3 Pro",
                        "price": 14999,
                        "currency": "CNY",
                        "stock": 5,
                        "rating": 4.9,
                        "seller": "Apple Store 官方旗舰店",
                        "warranty": "官方保修 1 年",
                        "shipping": "顺丰包邮，预计 2 天到达"
                    },
                    {
                        "id": "MBP-002",
                        "name": "MacBook Pro 16 M3 Max",
                        "price": 27999,
                        "currency": "CNY",
                        "stock": 3,
                        "rating": 4.95,
                        "seller": "Apple Store 官方旗舰店",
                        "warranty": "官方保修 1 年",
                        "shipping": "顺丰包邮，预计 2 天到达"
                    }
                ]
            }

        elif intent == "product.order":
            product = payload.get("product")
            quantity = payload.get("quantity", 1)
            print(f"   下单商品: {product['name']} x {quantity}")

            await asyncio.sleep(1)  # 模拟下单处理

            return {
                "intent": "product.order.confirmed",
                "order_id": "ORD-20260501-001",
                "status": "confirmed",
                "total": product["price"] * quantity,
                "estimated_delivery": "2026-05-03",
                "tracking": "SF1234567890"
            }

        elif intent == "product.order":
            product = payload.get("product")
            quantity = payload.get("quantity", 1)
            print(f"   下单商品: {product['name']} x {quantity}")

            await asyncio.sleep(1)  # 模拟下单处理

            return {
                "intent": "product.order.confirmed",
                "order_id": "ORD-20260501-003",
                "status": "confirmed",
                "total": product["price"] * quantity,
                "estimated_delivery": "2026-05-15",
                "tracking": "GL9876543210"
            }

        return {"message": "收到"}

    # 卖家 B - 第三方数码店
    async def handle_seller_b(msg):
        payload = msg.payload
        intent = payload.get("intent")

        print(f"\n💬 [{msg.receiver}] 收到消息:")
        print(f"   意图: {intent}")

        if intent == "product.search":
            product = payload.get("product", "")
            print(f"   搜索商品: {product}")
            await asyncio.sleep(0.5)

            return {
                "intent": "product.search.result",
                "products": [
                    {
                        "id": "MBP-003",
                        "name": "MacBook Pro 14 M3 Pro",
                        "price": 13999,
                        "currency": "CNY",
                        "stock": 2,
                        "rating": 4.7,
                        "seller": "极客数码旗舰店",
                        "warranty": "店铺保修 1 年",
                        "shipping": "京东物流，预计 1 天到达"
                    }
                ]
            }

        return {"message": "收到"}

    # 卖家 C - 跨境电商
    async def handle_seller_c(msg):
        payload = msg.payload
        intent = payload.get("intent")

        print(f"\n💬 [{msg.receiver}] 收到消息:")
        print(f"   意图: {intent}")

        if intent == "product.search":
            product = payload.get("product", "")
            print(f"   搜索商品: {product}")
            await asyncio.sleep(0.5)

            return {
                "intent": "product.search.result",
                "products": [
                    {
                        "id": "MBP-004",
                        "name": "MacBook Pro 14 M3 Pro (海外版)",
                        "price": 12999,
                        "currency": "CNY",
                        "stock": 8,
                        "rating": 4.6,
                        "seller": "全球购数码",
                        "warranty": "店铺保修 1 年",
                        "shipping": "跨境直邮，预计 7-15 天到达"
                    }
                ]
            }

        elif intent == "product.order":
            product = payload.get("product")
            quantity = payload.get("quantity", 1)
            print(f"   下单商品: {product['name']} x {quantity}")

            await asyncio.sleep(1)  # 模拟下单处理

            return {
                "intent": "product.order.confirmed",
                "order_id": "ORD-20260501-003",
                "status": "confirmed",
                "total": product["price"] * quantity,
                "estimated_delivery": "2026-05-15",
                "tracking": "GL9876543210"
            }

        return {"message": "收到"}

    # 创建三个卖家
    seller_a = Agent(name="apple-store", port=8766, capabilities=["product", "order"])
    seller_a.on_message(handle_seller_a)

    seller_b = Agent(name="geek-store", port=8770, capabilities=["product", "order"])
    seller_b.on_message(handle_seller_b)

    seller_c = Agent(name="global-store", port=8771, capabilities=["product", "order"])
    seller_c.on_message(handle_seller_c)

    # 注册到 Registry
    import websockets
    for seller in [seller_a, seller_b, seller_c]:
        async with websockets.connect("ws://localhost:8767") as ws:
            await ws.send(json.dumps({
                "action": "register",
                "uri": seller.uri,
                "name": seller.name,
                "capabilities": seller.capabilities
            }))
            await ws.recv()
        await seller.start()
        await asyncio.sleep(0.3)

    # 3. 启动买家 Agent
    buyer = Agent(name="buyer", port=8765, capabilities=["shopping", "comparison"])
    await buyer.start()
    await asyncio.sleep(0.5)

    # 4. 买家开始购物流程
    print("\n" + "=" * 60)
    print("👤 用户需求: 购买 MacBook Pro 14 M3 Pro")
    print("=" * 60)

    # 步骤 1: 搜索所有卖家
    print("\n" + "-" * 40)
    print("📋 步骤 1: 搜索商品")
    print("-" * 40)

    sellers = [
        ("agent://localhost:8766/apple-store", "Apple Store"),
        ("agent://localhost:8770/geek-store", "极客数码"),
        ("agent://localhost:8771/global-store", "全球购"),
    ]

    all_products = []
    for seller_uri, seller_name in sellers:
        print(f"\n🔍 搜索 {seller_name}...")
        response = await buyer.send_to(seller_uri, {
            "intent": "product.search",
            "product": "MacBook Pro 14 M3 Pro",
            "filters": {
                "max_price": 20000,
                "min_rating": 4.5
            }
        })
        if "products" in response:
            all_products.extend(response["products"])

    # 步骤 2: 比较价格
    print("\n" + "-" * 40)
    print("📊 步骤 2: 比较价格")
    print("-" * 40)

    all_products.sort(key=lambda x: x["price"])
    print("\n找到以下商品（按价格排序）：")
    print(f"{'排名':<4} {'商品名':<30} {'价格':<12} {'评分':<8} {'卖家'}")
    print("-" * 80)

    for i, p in enumerate(all_products, 1):
        print(f"{i:<4} {p['name']:<28} ¥{p['price']:<10} {p['rating']:<8} {p['seller']}")

    # 步骤 3: 智能推荐
    print("\n" + "-" * 40)
    print("🤖 步骤 3: 智能推荐")
    print("-" * 40)

    # 买家 Agent 分析
    best_value = min(all_products, key=lambda x: x["price"] / x["rating"])
    fastest_shipping = max(all_products, key=lambda x: x["stock"])

    print(f"\n💡 分析结果：")
    print(f"   🏆 性价比最高: {best_value['name']} (¥{best_value['price']}, 评分 {best_value['rating']})")
    print(f"   🚀 发货最快: {fastest_shipping['name']} (库存 {fastest_shipping['stock']} 件)")
    print(f"   💰 价格最低: {all_products[0]['name']} (¥{all_products[0]['price']})")

    # 步骤 4: 自动下单
    print("\n" + "-" * 40)
    print("🛒 步骤 4: 自动下单")
    print("-" * 40)

    selected = best_value  # 选择性价比最高的
    print(f"\n✅ 选择: {selected['name']}")
    print(f"   卖家: {selected['seller']}")
    print(f"   价格: ¥{selected['price']}")
    print(f"   评分: {selected['rating']}")

    # 找到对应的卖家 URI
    seller_map = {
        "Apple Store 官方旗舰店": "agent://localhost:8766/apple-store",
        "极客数码旗舰店": "agent://localhost:8770/geek-store",
        "全球购数码": "agent://localhost:8771/global-store",
    }
    order_seller = seller_map.get(selected["seller"])

    if order_seller:
        print(f"\n📦 向 {selected['seller']} 下单...")
        order_response = await buyer.send_to(order_seller, {
            "intent": "product.order",
            "product": selected,
            "quantity": 1,
            "payment_method": "支付宝",
            "shipping_address": "上海市黄浦区南京东路 100 号"
        })

        if order_response.get("status") == "confirmed":
            print(f"\n{'=' * 60}")
            print("🎉 下单成功！")
            print(f"{'=' * 60}")
            print(f"   订单号: {order_response['order_id']}")
            print(f"   总金额: ¥{order_response['total']}")
            print(f"   预计送达: {order_response['estimated_delivery']}")
            print(f"   物流单号: {order_response['tracking']}")
        else:
            print(f"\n❌ 下单失败: {order_response}")

    # 5. 完成
    print(f"\n{'=' * 60}")
    print("🎉 购物完成！")
    print(f"{'=' * 60}")
    print()
    print("总结:")
    print("  1. 买家 Agent 通过 Hub 发现多个卖家")
    print("  2. 自动搜索、比较价格和评分")
    print("  3. 智能推荐最优选择")
    print("  4. 自动完成下单")
    print()
    print("这就是 Agent 购物的未来！🚀")
    print()

    # 关闭所有
    await buyer.stop()
    await seller_a.stop()
    await seller_b.stop()
    await seller_c.stop()
    await registry.stop()


if __name__ == "__main__":
    asyncio.run(main())
