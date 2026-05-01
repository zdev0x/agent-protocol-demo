#!/usr/bin/env python3
"""
Agent Registry - 注册中心
Agent 启动时注册，其他 Agent 可以通过能力搜索找到
"""

import asyncio
import json
from datetime import datetime


class AgentRegistry:
    """
    Agent 注册中心 - 类似 DNS，帮助 Agent 发现彼此
    
    用法:
        registry = AgentRegistry(port=8766)
        await registry.start()  # 启动注册中心
    """
    
    def __init__(self, host: str = "localhost", port: int = 8766):
        self.host = host
        self.port = port
        self.agents: dict[str, dict] = {}  # uri -> agent_info
        self._server = None
    
    async def start(self):
        """启动注册中心"""
        import websockets
        self._server = await websockets.serve(
            self._handle_connection,
            self.host,
            self.port
        )
        print(f"📡 Agent Registry 启动成功")
        print(f"   地址: ws://{self.host}:{self.port}")
        print(f"   等待 Agent 注册...\n")
    
    async def _handle_connection(self, websocket):
        """处理请求"""
        try:
            async for raw in websocket:
                request = json.loads(raw)
                action = request.get("action")
                
                if action == "register":
                    # Agent 注册
                    uri = request["uri"]
                    info = {
                        "uri": uri,
                        "name": request["name"],
                        "capabilities": request.get("capabilities", []),
                        "registered_at": datetime.now().isoformat()
                    }
                    self.agents[uri] = info
                    
                    response = {"status": "ok", "message": f"已注册: {uri}"}
                    print(f"📝 新 Agent 注册: {uri}")
                    print(f"   能力: {info['capabilities']}")
                    
                elif action == "find":
                    # 搜索 Agent
                    capability = request.get("capability")
                    matched = [
                        a for a in self.agents.values()
                        if capability in a["capabilities"]
                    ]
                    response = {
                        "status": "ok",
                        "agents": [a["uri"] for a in matched]
                    }
                    print(f"🔍 搜索能力 [{capability}]: 找到 {len(matched)} 个")
                    
                elif action == "list":
                    # 列出所有 Agent
                    response = {
                        "status": "ok",
                        "agents": list(self.agents.keys())
                    }
                    
                else:
                    response = {"status": "error", "message": "未知操作"}
                
                await websocket.send(json.dumps(response))
                
        except Exception as e:
            print(f"Registry 错误: {e}")
    
    async def stop(self):
        if self._server:
            self._server.close()
            await self._server.wait_closed()
            print("📡 Registry 已停止")


async def main():
    """启动 Registry 服务"""
    registry = AgentRegistry()
    await registry.start()
    
    try:
        await asyncio.Future()  # 保持运行
    except KeyboardInterrupt:
        await registry.stop()


if __name__ == "__main__":
    asyncio.run(main())
