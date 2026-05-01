# RFC-001: Agent 通讯协议 (Agent Communication Protocol)

> 版本: 1.0.0-draft
> 日期: 2026-05-01
> 作者: zdev0x
> 状态: 草案

---

## 摘要

本文档定义了 Agent-to-Agent 通讯协议（ACP），一个用于 AI Agent 之间发现、连接和协作的开放标准。协议参考 TCP/IP 和 HTTP 的设计思想，旨在建立下一代 Agent 互联网的基础设施。

---

## 1. 引言

### 1.1 背景

当前 AI Agent 生态存在以下问题：

1. **孤岛化**：各框架（LangChain、CrewAI、AutoGen）之间无法互通
2. **缺乏标准**：Agent 间通讯格式自定义，无统一规范
3. **发现困难**：没有成熟的 Agent 发现和注册机制
4. **信任缺失**：Agent 间缺乏身份认证和能力验证

### 1.2 设计目标

- **开放性**：任何人都可以实现和部署
- **互操作性**：不同框架的 Agent 可以直接通讯
- **可扩展性**：支持未来新增功能和能力
- **安全性**：内置身份认证和消息加密

### 1.3 术语定义

| 术语 | 定义 |
|------|------|
| Agent | 能够自主执行任务的 AI 实体 |
| Agent Hub | Agent 注册和发现的中心服务 |
| Agent URI | Agent 的唯一标识符 |
| Capability | Agent 具备的能力描述 |
| Task | Agent 间协作的具体任务 |

---

## 2. 架构

### 2.1 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                     Agent Hub (Registry)                    │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   注册服务   │  │  发现服务   │  │    能力匹配引擎     │ │
│  │  Register   │  │   Discover  │  │  Capability Match   │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   Agent 目录                         │   │
│  │              (Agent Directory Store)                 │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↑
           ┌────────────────┼────────────────┐
           │                │                │
           │                │                │
   ┌───────▼───────┐ ┌─────▼───────┐ ┌───────▼───────┐
   │   Agent A     │ │   Agent B   │ │   Agent C     │
   │  (User)       │ │  (Service)  │ │  (Service)    │
   │               │ │             │ │               │
   │  URI:         │ │  URI:       │ │  URI:         │
   │  agent://...  │ │  agent://...│ │  agent://...  │
   │               │ │             │ │               │
   │  Capabilities:│ │Capabilities:│ │Capabilities:  │
   │  - user       │ │ - booking   │ │ - translation │
   │               │ │ - payment   │ │               │
   └───────────────┘ └─────────────┘ └───────────────┘
```

### 2.2 核心组件

1. **Agent Hub** - 中心化的注册和发现服务
2. **Agent** - 能够通讯的 AI 实体
3. **Agent URI** - 全球唯一的 Agent 标识符
4. **AgentMessage** - 标准化的消息格式

---

## 3. Agent URI 规范

### 3.1 格式定义

```
agent://{authority}/{agent-name}/{version}

其中:
- authority: 主机和端口，格式为 host:port 或 domain
- agent-name: Agent 名称，小写字母、数字、连字符
- version: API 版本，格式为 v{major}

示例:
agent://localhost:8765/alice/v1
agent://hub.agent.org/bob/v1
agent://api.openai.com/gpt-agent/v1
```

### 3.2 URI 组件说明

| 组件 | 必需 | 说明 |
|------|------|------|
| authority | 是 | Agent 所在的服务地址 |
| agent-name | 是 | Agent 的唯一名称 |
| version | 否 | API 版本，默认为 v1 |

### 3.3 特殊 URI

```
agent://hub/                  # 默认 Agent Hub
agent://broadcast/            # 广播地址
agent://capability/{name}     # 按能力查询
```

---

## 4. Agent Hub 规范

### 4.1 核心功能

Agent Hub 提供以下核心服务：

#### 4.1.1 注册服务 (Register)

Agent 启动时向 Hub 注册自己的信息。

**请求格式:**
```json
{
  "action": "register",
  "agent": {
    "uri": "agent://localhost:8765/alice/v1",
    "name": "alice",
    "capabilities": ["scheduling", "negotiation"],
    "description": "个人助理，擅长日程安排",
    "endpoint": "ws://localhost:8765",
    "metadata": {
      "version": "1.0.0",
      "author": "zdev0x"
    }
  }
}
```

**响应格式:**
```json
{
  "status": "ok",
  "message": "已注册: agent://localhost:8765/alice/v1",
  "agent_id": "alice-8765"
}
```

#### 4.1.2 发现服务 (Discover)

根据能力搜索 Agent。

**请求格式:**
```json
{
  "action": "discover",
  "query": {
    "capabilities": ["booking"],
    "min_reputation": 0.8,
    "max_latency": 1000,
    "limit": 10
  }
}
```

**响应格式:**
```json
{
  "status": "ok",
  "agents": [
    {
      "uri": "agent://localhost:8766/bob/v1",
      "name": "bob",
      "capabilities": ["booking", "scheduling"],
      "reputation": 0.95,
      "latency": 200,
      "endpoint": "ws://localhost:8766"
    }
  ],
  "total": 1
}
```

#### 4.1.3 心跳服务 (Heartbeat)

Agent 定期发送心跳，保持注册状态。

**请求格式:**
```json
{
  "action": "heartbeat",
  "agent_uri": "agent://localhost:8765/alice/v1"
}
```

**响应格式:**
```json
{
  "status": "ok",
  "ttl": 300
}
```

#### 4.1.4 注销服务 (Unregister)

Agent 停止时注销。

**请求格式:**
```json
{
  "action": "unregister",
  "agent_uri": "agent://localhost:8765/alice/v1"
}
```

---

## 5. AgentMessage 规范

### 5.1 消息格式

```json
{
  "id": "msg-a1b2c3d4",
  "version": "1.0",
  "type": "request|response|notification|error",
  "sender": {
    "uri": "agent://localhost:8765/alice/v1",
    "name": "alice"
  },
  "receiver": {
    "uri": "agent://localhost:8766/bob/v1",
    "name": "bob"
  },
  "payload": {
    "intent": "book_meeting",
    "data": {
      "proposed_time": "2026-05-02T14:00:00+08:00",
      "location": "上海"
    }
  },
  "metadata": {
    "timestamp": "2026-05-01T15:30:00Z",
    "ttl": 300,
    "priority": "normal",
    "reply_to": null,
    "conversation_id": "conv-xyz789"
  }
}
```

### 5.2 消息类型

| 类型 | 说明 |
|------|------|
| `request` | 请求消息，期望收到响应 |
| `response` | 响应消息，对应某个请求 |
| `notification` | 通知消息，不需要响应 |
| `error` | 错误消息 |

### 5.3 常用 Intent

#### 协作类

| Intent | 说明 |
|--------|------|
| `collaborate.request` | 请求协作 |
| `collaborate.accept` | 接受协作 |
| `collaborate.reject` | 拒绝协作 |
| `collaborate.complete` | 协作完成 |

#### 任务类

| Intent | 说明 |
|--------|------|
| `task.assign` | 分配任务 |
| `task.update` | 更新任务状态 |
| `task.complete` | 任务完成 |
| `task.cancel` | 取消任务 |

#### 支付类

| Intent | 说明 |
|--------|------|
| `payment.request` | 请求支付 |
| `payment.confirm` | 确认支付 |
| `payment.refund` | 退款 |

---

## 6. 通讯协议

### 6.1 传输层

支持以下传输协议：

| 协议 | 用途 | 优先级 |
|------|------|--------|
| WebSocket | 实时双向通讯 | 推荐 |
| HTTP/2 | 请求响应 | 备选 |
| gRPC | 高性能通讯 | 可选 |

### 6.2 连接建立

#### 6.2.1 握手流程

```
Agent A                     Agent B
   │                           │
   │──── Connect ─────────────→│
   │     (URI, Capabilities)   │
   │                           │
   │←──── Accept ──────────────│
   │     (URI, Capabilities)   │
   │                           │
   │──── Auth ────────────────→│
   │     (Signature)           │
   │                           │
   │←──── Auth OK ─────────────│
   │                           │
   │       连接建立完成         │
```

#### 6.2.2 认证方式

| 方式 | 说明 | 优先级 |
|------|------|--------|
| Token | API Token 认证 | 推荐 |
| Signature | 消息签名认证 | 可选 |
| TLS Client Cert | 客户端证书 | 可选 |

### 6.3 消息可靠性

#### 6.3.1 确认机制

```
发送方                    接收方
   │                        │
   │─── Message ────────────→│
   │                        │
   │←─── Ack (msg_id) ──────│
   │                        │
   │    (超时未收到则重试)    │
```

#### 6.3.2 重试策略

| 参数 | 默认值 | 说明 |
|------|--------|------|
| max_retries | 3 | 最大重试次数 |
| retry_interval | 1000ms | 重试间隔 |
| backoff_multiplier | 2 | 退避倍数 |

### 6.4 流量控制

| 参数 | 默认值 | 说明 |
|------|--------|------|
| max_concurrent | 10 | 最大并发请求数 |
| rate_limit | 100/s | 每秒最大请求数 |
| message_size_limit | 1MB | 单条消息最大大小 |

---

## 7. 能力描述规范

### 7.1 能力格式

```json
{
  "name": "booking",
  "version": "1.0",
  "description": "预订服务",
  "parameters": {
    "type": "booking|cancellation|modification",
    "service": "flight|hotel|restaurant|ticket"
  },
  "output": {
    "confirmation_code": "string",
    "status": "confirmed|pending|failed"
  }
}
```

### 7.2 内置能力类型

| 能力 | 说明 |
|------|------|
| `booking` | 预订服务 |
| `payment` | 支付服务 |
| `translation` | 翻译服务 |
| `search` | 搜索服务 |
| `computation` | 计算服务 |
| `storage` | 存储服务 |

### 7.3 自定义能力

Agent 可以注册自定义能力，只需遵循能力格式规范。

---

## 8. 安全规范

### 8.1 身份验证

#### 8.1.1 Agent 身份

每个 Agent 必须有唯一的身份标识：

```json
{
  "identity": {
    "uri": "agent://localhost:8765/alice/v1",
    "public_key": "-----BEGIN PUBLIC KEY-----\n...",
    "signature_algorithm": "RSA-SHA256"
  }
}
```

#### 8.1.2 消息签名

每条消息必须包含签名：

```json
{
  "signature": {
    "algorithm": "RSA-SHA256",
    "value": "base64_encoded_signature",
    "signed_fields": ["id", "sender", "receiver", "payload", "timestamp"]
  }
}
```

### 8.2 消息加密

支持以下加密方式：

| 方式 | 说明 | 优先级 |
|------|------|--------|
| TLS 1.3 | 传输层加密 | 必需 |
| E2E | 端到端加密 | 推荐 |
| Payload | 消息体加密 | 可选 |

### 8.3 访问控制

Agent Hub 支持以下访问控制策略：

```json
{
  "access_control": {
    "allowed_agents": ["agent://trusted/*"],
    "blocked_agents": [],
    "capability_whitelist": ["booking", "payment"],
    "rate_limits": {
      "per_agent": 100,
      "per_minute": 1000
    }
  }
}
```

---

## 9. 错误处理

### 9.1 错误码

| 错误码 | 说明 |
|--------|------|
| 400 | 请求格式错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | Agent 不存在 |
| 408 | 请求超时 |
| 429 | 请求过多 |
| 500 | 服务器错误 |

### 9.2 错误消息格式

```json
{
  "type": "error",
  "error": {
    "code": 404,
    "message": "Agent not found",
    "details": {
      "agent_uri": "agent://localhost:8766/bob/v1"
    }
  }
}
```

---

## 10. 扩展机制

### 10.1 协议扩展

通过 `extensions` 字段支持协议扩展：

```json
{
  "extensions": {
    "payment": {
      "version": "1.0",
      "enabled": true
    },
    "encryption": {
      "algorithm": "AES-256-GCM"
    }
  }
}
```

### 10.2 能力扩展

Agent 可以动态注册新能力，无需修改协议。

---

## 11. 实现参考

### 11.1 Python SDK

```python
from agent_protocol import Agent, Hub

# 连接到 Hub
hub = Hub("ws://hub.agent.org")

# 创建 Agent
agent = Agent(
    name="alice",
    capabilities=["booking", "scheduling"]
)

# 注册到 Hub
await hub.register(agent)

# 发现其他 Agent
agents = await hub.discover(capability="payment")

# 发送消息
response = await agent.send_to(
    target="agent://localhost:8766/bob/v1",
    intent="book_meeting",
    data={"time": "2026-05-02T14:00:00Z"}
)
```

### 11.2 JavaScript SDK

```javascript
import { Agent, Hub } from 'agent-protocol';

// 连接到 Hub
const hub = new Hub('ws://hub.agent.org');

// 创建 Agent
const agent = new Agent({
  name: 'alice',
  capabilities: ['booking', 'scheduling']
});

// 注册到 Hub
await hub.register(agent);

// 发现其他 Agent
const agents = await hub.discover({ capability: 'payment' });

// 发送消息
const response = await agent.sendTo({
  target: 'agent://localhost:8766/bob/v1',
  intent: 'book_meeting',
  data: { time: '2026-05-02T14:00:00Z' }
});
```

---

## 12. 未来工作

### 12.1 短期计划

- [ ] 完善 Agent Hub 实现
- [ ] 添加消息加密支持
- [ ] 实现分布式 Registry
- [ ] 编写完整测试套件

### 12.2 中期计划

- [ ] 发布 Python/JS SDK
- [ ] 与 LangChain/CrewAI 集成
- [ ] 建立 Agent Marketplace
- [ ] 支持 Agent 支付

### 12.3 长期愿景

- [ ] 成为 Agent 通讯的行业标准
- [ ] 建立全球 Agent 互联网
- [ ] 支持万亿级 Agent 互联

---

## 13. 变更记录

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| 1.0.0-draft | 2026-05-01 | 初始草案 |

---

## 14. 参考资料

- [TCP/IP 协议规范](https://tools.ietf.org/html/rfc793)
- [HTTP/2 协议规范](https://tools.ietf.org/html/rfc7540)
- [WebSocket 协议规范](https://tools.ietf.org/html/rfc6455)
- [Google A2A 协议](https://github.com/a2aproject/A2A)
- [MCP 协议](https://modelcontextprotocol.io)

---

<p align="center">
  <strong>📝 RFC-001: Agent 通讯协议 v1.0.0-draft</strong><br>
  <em>让我们一起构建下一代 Agent 互联网</em>
</p>
