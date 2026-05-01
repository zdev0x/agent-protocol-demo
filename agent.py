"""
Agent 通讯协议 - 核心模块

本模块实现了 Agent-to-Agent 通讯协议的核心组件：
- AgentMessage: 标准化消息格式
- Agent: Agent 基类，支持 WebSocket 通讯

协议设计参考 TCP/IP 和 HTTP，详见 RFC-001。

作者: zdev0x
版本: 1.0.0
日期: 2026-05-01
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Optional, Callable


class AgentMessage:
    """
    Agent 消息格式
    
    所有 Agent 间的通讯都使用统一的消息格式，确保互操作性。
    
    消息结构:
    {
        "id": "消息唯一标识",
        "sender": "发送者 URI",
        "receiver": "接收者 URI",
        "type": "消息类型 (request/response/notification/error)",
        "payload": "消息内容",
        "timestamp": "发送时间"
    }
    
    示例:
        msg = AgentMessage(
            sender="agent://localhost:8765/alice",
            receiver="agent://localhost:8766/bob",
            msg_type="request",
            payload={"intent": "book_meeting", "time": "tomorrow"}
        )
    """
    
    def __init__(self, sender: str, receiver: str, msg_type: str, payload: dict):
        """
        初始化消息
        
        Args:
            sender: 发送者 Agent URI
            receiver: 接收者 Agent URI
            msg_type: 消息类型 (request/response/notification/error)
            payload: 消息内容字典
        """
        self.id = str(uuid.uuid4())[:8]  # 8 位唯一 ID
        self.sender = sender
        self.receiver = receiver
        self.type = msg_type
        self.payload = payload
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """将消息转换为字典格式"""
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "type": self.type,
            "payload": self.payload,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AgentMessage':
        """从字典创建消息"""
        msg = cls(
            sender=data["sender"],
            receiver=data["receiver"],
            msg_type=data["type"],
            payload=data["payload"]
        )
        msg.id = data.get("id", msg.id)
        msg.timestamp = data.get("timestamp", msg.timestamp)
        return msg
    
    def __repr__(self) -> str:
        return f"[{self.type}] {self.sender} → {self.receiver}: {self.payload}"


class Agent:
    """
    Agent 基类 - 支持 WebSocket 通讯
    
    每个 Agent 都有一个唯一的 URI 地址，可以通过 WebSocket 与其他 Agent 通讯。
    
    Agent URI 格式:
        agent://{host}:{port}/{name}
    
    示例:
        agent://localhost:8765/alice
        agent://localhost:8766/bob
    
    使用方法:
        # 创建 Agent
        agent = Agent(
            name="alice",
            port=8765,
            capabilities=["scheduling", "negotiation"]
        )
        
        # 注册消息处理器
        agent.on_message(handler)
        
        # 启动服务
        await agent.start()
        
        # 发送消息
        response = await agent.send_to(
            target_uri="agent://localhost:8766/bob",
            payload={"intent": "greet", "message": "Hello!"}
        )
    """
    
    def __init__(self, name: str, host: str = "localhost", port: int = 8765, 
                 capabilities: list = None):
        """
        初始化 Agent
        
        Args:
            name: Agent 名称，用于 URI 中
            host: 主机地址，默认 localhost
            port: 端口号，默认 8765
            capabilities: Agent 能力列表，如 ["booking", "payment"]
        """
        self.name = name
        self.host = host
        self.port = port
        self.uri = f"agent://{host}:{port}/{name}"  # Agent 唯一标识
        self.capabilities = capabilities or []
        
        self._handler: Optional[Callable] = None  # 消息处理器
        self._server = None  # WebSocket 服务器
    
    def on_message(self, handler: Callable):
        """
        注册消息处理函数
        
        当收到其他 Agent 的消息时，会调用此函数处理。
        
        Args:
            handler: 异步处理函数，接收 AgentMessage，返回响应字典
        """
        self._handler = handler
    
    async def start(self):
        """
        启动 Agent 服务
        
        启动 WebSocket 服务器，等待其他 Agent 连接。
        """
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
    
    async def _handle_connection(self, websocket):
        """
        处理 WebSocket 连接
        
        当其他 Agent 连接时，接收消息并调用处理器。
        
        Args:
            websocket: WebSocket 连接对象
        """
        import websockets as ws_lib
        try:
            async for raw in websocket:
                # 解析消息
                data = json.loads(raw)
                msg = AgentMessage.from_dict(data)
                
                # 调用注册的处理器
                if self._handler:
                    response = await self._handler(msg)
                    if response:
                        # 包装成标准消息格式回复
                        resp_msg = AgentMessage(
                            sender=msg.receiver,
                            receiver=msg.sender,
                            msg_type="response",
                            payload=response if isinstance(response, dict) else {"result": response}
                        )
                        await websocket.send(json.dumps(resp_msg.to_dict()))
        except ws_lib.exceptions.ConnectionClosed:
            # 连接正常关闭
            pass
        except Exception as e:
            print(f"   ⚠️ 处理消息出错: {e}")
    
    async def send_to(self, target_uri: str, payload: dict, msg_type: str = "request") -> dict:
        """
        发送消息给目标 Agent
        
        Args:
            target_uri: 目标 Agent URI，如 agent://localhost:8766/bob
            payload: 消息内容
            msg_type: 消息类型，默认 request
            
        Returns:
            响应 payload 字典
        """
        import websockets
        
        # 解析 URI: agent://host:port/name
        target = target_uri.replace("agent://", "")
        host_port, name = target.rsplit("/", 1)
        host, port = host_port.split(":")
        port = int(port)
        
        try:
            async with websockets.connect(f"ws://{host}:{port}") as ws:
                # 构造消息
                msg = AgentMessage(
                    sender=self.name,
                    receiver=name,
                    msg_type=msg_type,
                    payload=payload
                )
                
                print(f"\n📤 [{self.name}] 发送消息:")
                print(f"   目标: {target_uri}")
                print(f"   内容: {json.dumps(payload, ensure_ascii=False, indent=2)}")
                
                # 发送消息
                await ws.send(json.dumps(msg.to_dict()))
                
                # 等待响应（超时 30 秒）
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
        """停止 Agent 服务"""
        if self._server:
            self._server.close()
            await self._server.wait_closed()
            print(f"🤖 Agent [{self.name}] 已停止")
