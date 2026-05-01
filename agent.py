#!/usr/bin/env python3
"""
Agent 通讯协议 - 基类
支持 Agent 间通过 WebSocket 发现和对话
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Optional, Callable


class AgentMessage:
    """Agent 消息格式"""
    
    def __init__(self, sender: str, receiver: str, msg_type: str, payload: dict):
        self.id = str(uuid.uuid4())[:8]
        self.sender = sender
        self.receiver = receiver
        self.type = msg_type  # request, response, confirm
        self.payload = payload
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "type": self.type,
            "payload": self.payload,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        msg = cls(
            sender=data["sender"],
            receiver=data["receiver"],
            msg_type=data["type"],
            payload=data["payload"]
        )
        msg.id = data.get("id", msg.id)
        msg.timestamp = data.get("timestamp", msg.timestamp)
        return msg
    
    def __repr__(self):
        return f"[{self.type}] {self.sender} → {self.receiver}: {self.payload}"


class Agent:
    """
    Agent 基类 - 支持 WebSocket 通讯
    
    用法:
        agent = Agent(name="assistant", port=8765)
        agent.on_message(handler)  # 注册消息处理器
        await agent.start()        # 启动服务
        await agent.send_to("agent://localhost:8766", {...})  # 发送消息
    """
    
    def __init__(self, name: str, host: str = "localhost", port: int = 8765, 
                 capabilities: list = None):
        self.name = name
        self.host = host
        self.port = port
        self.uri = f"agent://{host}:{port}/{name}"
        self.capabilities = capabilities or []
        
        self._handler: Optional[Callable] = None
        self._server = None
        self._connections: dict[str, asyncio.Queue] = {}
    
    def on_message(self, handler: Callable):
        """注册消息处理函数"""
        self._handler = handler
    
    async def start(self):
        """启动 Agent 服务"""
        import websockets
        self._server = await websockets.serve(
            self._handle_connection, 
            self.host, 
            self.port
        )
        print(f"🤖 Agent [{self.name}] 启动成功")
        print(f"   URI: {self.uri}")
        print(f"   能力: {self.capabilities}")
        print(f"   等待连接...\n")
    
    async def _handle_connection(self, websocket, path):
        """处理 WebSocket 连接"""
        try:
            async for raw in websocket:
                data = json.loads(raw)
                msg = AgentMessage.from_dict(data)
                
                # 调用注册的处理器
                if self._handler:
                    response = await self._handler(msg)
                    if response:
                        await websocket.send(json.dumps(response.to_dict()))
        except websockets.exceptions.ConnectionClosed:
            pass
    
    async def send_to(self, target_uri: str, payload: dict, msg_type: str = "request") -> dict:
        """
        发送消息给目标 Agent
        
        target_uri: agent://host:port/name
        payload: 消息内容
        返回: 响应 payload
        """
        import websockets
        
        # 解析 URI: agent://host:port/name
        target = target_uri.replace("agent://", "")
        host, port, name = target.split(":")
        port = int(port)
        
        try:
            async with websockets.connect(f"ws://{host}:{port}") as ws:
                msg = AgentMessage(
                    sender=self.name,
                    receiver=name,
                    msg_type=msg_type,
                    payload=payload
                )
                
                print(f"\n📤 [{self.name}] 发送消息:")
                print(f"   目标: {target_uri}")
                print(f"   内容: {json.dumps(payload, ensure_ascii=False, indent=2)}")
                
                await ws.send(json.dumps(msg.to_dict()))
                
                # 等待响应
                response_raw = await asyncio.wait_for(ws.recv(), timeout=30)
                response = json.loads(response_raw)
                
                print(f"\n📥 [{self.name}] 收到响应:")
                print(f"   内容: {json.dumps(response['payload'], ensure_ascii=False, indent=2)}")
                
                return response["payload"]
                
        except asyncio.TimeoutError:
            print(f"❌ 请求超时")
            return {"error": "timeout"}
        except ConnectionRefusedError:
            print(f"❌ 无法连接到 {target_uri}")
            return {"error": "connection_refused"}
    
    async def stop(self):
        """停止 Agent"""
        if self._server:
            self._server.close()
            await self._server.wait_closed()
            print(f"🤖 Agent [{self.name}] 已停止")
