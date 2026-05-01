<p align="center">
  <h1 align="center">🚀 Agent Protocol</h1>
  <p align="center">
    <strong>下一代 Agent-to-Agent 通讯协议</strong><br>
    让 AI Agent 们自己互相聊天，人类只看结果
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/WebSocket-实时通讯-green" alt="WebSocket">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>

---

## 💡 这是什么？

当前 AI Agent 的协作模式：
```
人 → Agent → 工具 (MCP)
```

**我们要做的：**
```
人 → Agent ↔ Agent → 人
```

**核心愿景**：教 AI Agent 们自己互相聊天，人类只看结果。

---

## 🎬 Demo 演示

两个 Agent 自动协商约饭：

```
👤 Alice: "我想约明天下午吃饭"
   ↓
🤖 Agent A → Registry → 找到能"订餐"的 Agent
   ↓
🤖 Agent B 收到请求 → 思考中...
   ↓
🤖 Agent B: "好的！推荐海底捞 🍲"
   ↓
👤 Alice: "收到，明天见！"
   ↓
🎉 约饭成功！
```

---

## 🏗️ 架构设计

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
    "message": "想约明天吃饭",
    "proposed_time": "明天 14:00"
  },
  "timestamp": "2026-05-01T15:30:00"
}
```

### 系统架构图

```
┌─────────────────────────────────────────────────┐
│                 Agent Registry                  │
│              (ws://localhost:8767)               │
│         负责 Agent 发现和能力搜索                 │
│                                                 │
│   📡 register()   🔍 find(capability)   📋 list() │
└─────────────────────────────────────────────────┘
                           ↑
              ┌────────────┴────────────┐
              │                         │
    ┌─────────▼──────────┐   ┌──────────▼─────────┐
    │     Agent A        │   │      Agent B       │
    │   (Alice:8765)     │   │     (Bob:8766)     │
    │                    │   │                    │
    │   能力:            │   │   能力:            │
    │   - scheduling     │   │   - booking        │
    │   - negotiation    │   │   - scheduling     │
    │                    │   │                    │
    └─────────┬──────────┘   └──────────┬─────────┘
              │                         │
              └──────── WebSocket ───────┘
                   Agent ↔ Agent 通讯
```

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/zdev0x/agent-protocol-demo.git
cd agent-protocol-demo
```

### 2. 安装依赖

```bash
python3 -m venv venv
source venv/bin/activate
pip install websockets
```

### 3. 运行 Demo

```bash
python3 run_demo.py
```

### 4. 查看效果

```
============================================================
🚀 Agent 通讯协议 Demo
============================================================

📡 Agent Registry 启动成功
   地址: ws://localhost:8767

📝 新 Agent 注册: agent://localhost:8766/bob
🤖 Agent [bob] 启动成功

📝 新 Agent 注册: agent://localhost:8765/alice
🤖 Agent [alice] 启动成功

============================================================
🍽️  Alice 向 Bob 发起约饭请求
============================================================

🔍 搜索能力 [booking]: 找到 1 个
📤 [alice] 发送消息:
   意图: book_meeting
   提议: 明天 14:00

💬 [bob] 收到消息
🤔 思考中...
   → 回复: 同意，推荐地点

📥 [alice] 收到响应:
   "同意！推荐地点: 上海人民广场海底捞 🍲"

✅ 约饭成功！
============================================================
```

---

## 📁 项目结构

```
agent-protocol-demo/
├── agent.py          # Agent 基类（核心）
│                     #   - WebSocket 通讯
│                     #   - 消息格式定义
│                     #   - URI 解析
│
├── registry.py       # Agent 注册中心
│                     #   - Agent 注册
│                     #   - 能力搜索
│
├── agent_a.py        # Agent A（独立运行版）
│                     #   - 发起约饭请求
│
├── agent_b.py        # Agent B（独立运行版）
│                     #   - 接收并响应请求
│
├── run_demo.py       # 一键运行 Demo
│                     #   - 启动所有组件
│
└── README.md         # 项目文档
```

---

## 🔧 独立运行（双终端模式）

如果你想看两个独立进程通讯：

**终端 1 - 启动 Registry + Agent B:**

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动 Registry（后台）
python3 registry.py &

# 启动 Agent B（响应方）
python3 agent_b.py
```

**终端 2 - 启动 Agent A:**

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动 Agent A（发起方）
python3 agent_a.py
```

---

## 🧠 设计参考

本协议设计参考了 **TCP/IP** 和 **HTTP** 的思想：

| TCP/IP 概念 | Agent 通讯对应 | 说明 |
|------------|---------------|------|
| IP 地址 | Agent URI | 全球唯一标识一个 Agent |
| DNS | Agent Registry | 发现目标 Agent |
| TCP 三次握手 | Agent 认证 | 建立连接、协商能力 |
| HTTP 请求 | AgentMessage | 标准化消息格式 |
| 流量控制 | 速率限制 | 防止 Agent 过载 |

### 与现有协议的关系

| 协议 | 定位 | 方向 |
|------|------|------|
| **MCP** | Agent ↔ 工具 | 纵向（调用工具）|
| **A2A** | Agent ↔ Agent | 横向（协作对话）|
| **本协议** | Agent ↔ Agent | 横向 + 发现机制 |

**结论**：MCP 和 Agent 通讯是**互补关系**，不是竞争。

---

## 🗺️ Roadmap

### Phase 1: 基础协议 ✅
- [x] Agent 基类
- [x] 消息格式定义
- [x] Agent Registry
- [x] 基础 Demo

### Phase 2: 核心功能
- [ ] 消息加密 (TLS/SSL)
- [ ] 心跳检测
- [ ] 消息持久化
- [ ] 重试机制

### Phase 3: 分布式
- [ ] 分布式 Registry
- [ ] 消息路由
- [ ] Agent 负载均衡
- [ ] 跨网络通讯

### Phase 4: 生态
- [ ] Python SDK
- [ ] JavaScript SDK
- [ ] 与 LangChain/CrewAI 集成
- [ ] Agent Marketplace

---

## 🤝 参与贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 📄 License

MIT License - 详见 [LICENSE](LICENSE)

---

<p align="center">
  <strong>⭐ 如果觉得有用，请给个 Star 支持一下！</strong>
</p>
