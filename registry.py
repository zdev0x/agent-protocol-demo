"""
Agent Registry - 注册中心

本模块实现了 Agent 注册和发现服务：
- Agent 注册：Agent 启动时向 Registry 注册自己
- Agent 发现：根据能力搜索 Agent
- 心跳管理：Agent 定期发送心跳保持注册状态

类比互联网：
- Registry = DNS（域名解析）
- 注册 = 添加 DNS 记录
- 发现 = DNS 查询

作者: zdev0x
版本: 1.0.0
日期: 2026-05-01
"""

import asyncio
import json
from datetime import datetime


class AgentRegistry:
    """
    Agent 注册中心
    
    负责 Agent 的注册、发现和管理。
    
    使用方法:
        registry = AgentRegistry(port=8767)
        await registry.start()
        
        # Agent 注册
        await registry.register(agent_info)
        
        # 搜索 Agent
        agents = await registry.discover(capability="booking")
    """
    
    def __init__(self, host: str = "localhost", port: int = 8766):
        """
        初始化注册中心
        
        Args:
            host: 主机地址
            port: 端口号
        """
        self.host = host
        self.port = port
        self.agents: dict[str, dict] = {}  # URI -> Agent 信息
        self._server = None
    
    async def start(self):
        """启动注册中心服务"""
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
        """
        处理请求
        
        支持以下操作：
        - register: Agent 注册
        - find: 搜索 Agent
        - list: 列出所有 Agent
        - unregister: 注销 Agent
        """
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
                    
                elif action == "unregister":
                    # 注销 Agent
                    uri = request.get("uri")
                    if uri in self.agents:
                        del self.agents[uri]
                        response = {"status": "ok", "message": f"已注销: {uri}"}
                        print(f"❌ Agent 注销: {uri}")
                    else:
                        response = {"status": "error", "message": "Agent 不存在"}
                    
                else:
                    response = {"status": "error", "message": "未知操作"}
                
                await websocket.send(json.dumps(response))
                
        except Exception as e:
            print(f"Registry 错误: {e}")
    
    async def stop(self):
        """停止注册中心"""
        if self._server:
            self._server.close()
            await self._server.wait_closed()
            print("📡 Registry 已停止")


async def main():
    """启动 Registry 服务（独立运行时使用）"""
    registry = AgentRegistry()
    await registry.start()
    
    try:
        await asyncio.Future()  # 保持运行
    except KeyboardInterrupt:
        await registry.stop()


if __name__ == "__main__":
    asyncio.run(main())
