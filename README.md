# 🚀 Agent 通讯协议 Demo

> 两个 AI Agent 通过 WebSocket 自动协商约饭的演示

## 核心概念

### Agent URI（统一地址格式）
```
agent://{host}:{port}/{name}

示例:
agent://localhost:8765/alice
agent://localhost:8766/bob
```

### 消息格式 (AgentMessage)
```json
{
  "id": "a1b2c3d4",
  "sender": "alice",
  "receiver": "bob", 
  "type": "request",
  "payload": {
    "intent": "book_meeting",
    "message": "想约明天吃饭"
  },
  "timestamp": "2026-05-01T15:30:00"
}
```

### 架构图
```
┌─────────────────────────────────────────────────┐
│                  Agent Registry                 │
│              (ws://localhost:8766)               │
│         负责 Agent 发现和能力搜索                  │
└─────────────────────────────────────────────────┘
                           ↑
              ┌────────────┴────────────┐
              │                         │
    ┌─────────▼──────────┐   ┌──────────▼─────────┐
    │     Agent A        │   │      Agent B       │
    │   (Alice:8765)     │   │     (Bob:8766)     │
    │   能力: scheduling  │   │    能力: booking   │
    │        ↕           │   │         ↕          │
    │   WebSocket 通讯    │←→│    WebSocket 通讯   │
    └────────────────────┘   └────────────────────┘
```

## 快速开始

### 1. 安装依赖
```bash
python3 -m venv venv
source venv/bin/activate
pip install websockets
```

### 2. 运行 Demo
```bash
python3 run_demo.py
```

### 3. 查看输出
```
🚀 Agent 通讯协议 Demo

📡 Agent Registry 启动成功

🤖 Agent [bob] 启动成功
   URI: agent://localhost:8766/bob
   能力: ['booking', 'scheduling']

🤖 Agent [alice] 启动成功  
   URI: agent://localhost:8765/alice
   能力: ['scheduling', 'negotiation']

🔍 通过 Registry 找到: agent://localhost:8766/bob

📤 [alice] 发送消息:
   意图: book_meeting
   提议: 明天 14:00

📥 [bob] 收到消息:
   → 回复: 同意，推荐地点

✅ 约饭成功！
   时间: 明天 14:00
   地点: 上海人民广场海底捞 🍲
```

## 项目结构

```
agent-protocol-demo/
├── agent.py          # Agent 基类（核心）
├── registry.py       # Agent 注册中心
├── agent_a.py        # Agent A（独立运行版）
├── agent_b.py        # Agent B（独立运行版）
├── run_demo.py       # 一键运行 Demo
└── README.md
```

## 独立运行（双终端模式）

如果你想看两个独立进程通讯：

**终端 1 - 启动 Registry + Agent B:**
```bash
python3 registry.py &
python3 agent_b.py
```

**终端 2 - 启动 Agent A:**
```bash
python3 agent_a.py
```

## 设计参考

本协议设计参考了 TCP/IP 和 HTTP 的思想：

| TCP/IP | Agent 通讯 |
|--------|-----------|
| IP 地址 | Agent URI |
| DNS | Agent Registry |
| TCP 握手 | Agent 认证 |
| HTTP 请求 | AgentMessage |
| 流量控制 | 速率限制 |

## 下一步

- [ ] 实现消息加密 (TLS)
- [ ] 添加消息持久化
- [ ] 支持多 Agent 路由
- [ ] 实现 Agent 能力协商
- [ ] 添加心跳检测
- [ ] 分布式 Registry

## License

MIT
