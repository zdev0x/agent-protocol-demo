# RFC-001: Agent Communication Protocol (ACP) v0.1

> 版本: 0.1.0-draft
> 日期: 2026-05-01
> 作者: zdev0x
> 状态: 草案

---

## 1. 摘要

ACP (Agent Communication Protocol) 是一个轻量级 Agent 通信协议草案，目标是为个人开发者、中小团队和私有化 Agent 系统提供简单、可实现、低依赖的 Agent 注册、发现和协作规范。

**ACP 不是替代 A2A 或 MCP**，而是提供一个更容易理解、实现和二次开发的轻量协议。

---

## 2. 定位

### 2.1 ACP 是什么

```
ACP = Agent 的"HTTP"
```

就像 HTTP 让网页之间可以通讯，ACP 让 Agent 之间可以通讯。

### 2.2 ACP 不是什么

```
❌ 不是 A2A 的替代品
❌ 不是 MCP 的替代品
❌ 不是全球 Agent 互联网标准
❌ 不是企业级生产协议
```

### 2.3 适用场景

```
✅ 个人开发者学习 Agent 通讯
✅ 私有化 Agent 系统内部通讯
✅ 中小规模 Agent 网络
✅ Agent 协议教学和研究
✅ 快速原型验证
```

### 2.4 与现有协议的关系

| 协议 | 定位 | 关系 |
|------|------|------|
| **MCP** | LLM ↔ 工具/数据 | 互补，ACP 不涉及工具调用 |
| **A2A** | Agent ↔ Agent 互操作 | ACP 是简化版/学习版 |
| **ACP** | Agent ↔ Agent 通讯 | 轻量级，易实现 |

---

## 3. 核心设计

### 3.1 设计原则

```
1. 简单性 - 最小化概念，易于理解
2. 可实现 - 一个开发者能独立实现
3. 低依赖 - 只需 WebSocket 或 HTTP
4. 可扩展 - 核心精简，扩展可选
5. 实用性 - 解决真实问题
```

### 3.2 架构

```
┌─────────────────────────────────────────┐
│           Agent Registry               │
│        (可选，支持去中心化)              │
│                                         │
│   register / discover / heartbeat       │
└─────────────────────────────────────────┘
                    ↑
       ┌────────────┴────────────┐
       │                         │
┌──────▼──────┐           ┌──────▼──────┐
│   Agent A   │           │   Agent B   │
│             │           │             │
│  send_task  │──────────→│  get_status │
│  get_status │←──────────│  accept     │
└─────────────┘           └─────────────┘
```

---

## 4. 核心规范 (v0.1)

ACP v0.1 只定义 4 个核心动作：

### 4.1 register - 注册

Agent 向 Registry 注册自己。

**请求:**
```json
{
  "action": "register",
  "agent": {
    "agent_id": "booking-agent-001",
    "name": "Booking Agent",
    "description": "处理酒店和机票预订",
    "version": "1.0.0",
    "endpoint": "https://example.com/acp/agent",
    "capabilities": [
      {
        "name": "booking.hotel",
        "description": "预订酒店"
      },
      {
        "name": "booking.flight", 
        "description": "预订机票"
      }
    ],
    "auth": {
      "type": "bearer"
    }
  }
}
```

**响应:**
```json
{
  "status": "ok",
  "agent_id": "booking-agent-001",
  "registered_at": "2026-05-01T15:30:00Z"
}
```

### 4.2 discover - 发现

根据能力搜索 Agent。

**请求:**
```json
{
  "action": "discover",
  "query": {
    "capability": "booking.hotel",
    "limit": 10
  }
}
```

**响应:**
```json
{
  "status": "ok",
  "agents": [
    {
      "agent_id": "booking-agent-001",
      "name": "Booking Agent",
      "endpoint": "https://example.com/acp/agent",
      "capabilities": ["booking.hotel", "booking.flight"],
      "auth": {
        "type": "bearer"
      }
    }
  ]
}
```

### 4.3 send_task - 发送任务

向 Agent 发送任务。

**请求:**
```json
{
  "action": "send_task",
  "task": {
    "task_id": "task-20260501-001",
    "type": "booking.hotel",
    "input": {
      "city": "上海",
      "check_in": "2026-05-15",
      "check_out": "2026-05-17",
      "guests": 2
    },
    "metadata": {
      "requester": "user-agent-001",
      "timeout": 300
    }
  }
}
```

**响应:**
```json
{
  "status": "ok",
  "task_id": "task-20260501-001",
  "accepted": true
}
```

### 4.4 get_status - 查询状态

查询任务执行状态。

**请求:**
```json
{
  "action": "get_status",
  "task_id": "task-20260501-001"
}
```

**响应:**
```json
{
  "status": "ok",
  "task": {
    "task_id": "task-20260501-001",
    "state": "completed",
    "result": {
      "hotel": "上海外滩华尔道夫",
      "room_type": "豪华江景房",
      "price": 2800,
      "currency": "CNY",
      "confirmation": "WAL-20260515-001"
    },
    "created_at": "2026-05-01T15:30:00Z",
    "completed_at": "2026-05-01T15:30:05Z"
  }
}
```

---

## 5. 任务状态机

### 5.1 状态定义

```
created → accepted → running → completed
                    ↘ failed
                    ↘ cancelled
                    ↘ expired
```

| 状态 | 说明 |
|------|------|
| `created` | 任务已创建，等待 Agent 接收 |
| `accepted` | Agent 已接受任务 |
| `running` | 任务执行中 |
| `completed` | 任务完成 |
| `failed` | 任务失败 |
| `cancelled` | 任务取消 |
| `expired` | 任务超时 |

### 5.2 状态转换规则

```
created → accepted     (Agent 接受)
created → failed       (Agent 拒绝)
accepted → running     (开始执行)
accepted → cancelled   (用户取消)
running → completed    (执行完成)
running → failed       (执行失败)
running → cancelled    (用户取消)
```

---

## 6. 传输层

### 6.1 支持的传输协议

| 协议 | 优先级 | 说明 |
|------|--------|------|
| HTTP + JSON | 推荐 | 简单，兼容性好 |
| WebSocket | 可选 | 实时双向通讯 |

### 6.2 端点规范

```
Registry 端点:
  POST /acp/register      # 注册
  POST /acp/discover      # 发现
  POST /acp/heartbeat     # 心跳

Agent 端点:
  POST /acp/task          # 发送任务
  GET  /acp/task/{id}     # 查询状态
  POST /acp/task/{id}/cancel  # 取消任务
```

---

## 7. 错误处理

### 7.1 错误格式

```json
{
  "status": "error",
  "error": {
    "code": "AGENT_NOT_FOUND",
    "message": "Agent not found"
  }
}
```

### 7.2 错误码

| 错误码 | 说明 | 可重试 |
|--------|------|--------|
| `AGENT_NOT_FOUND` | Agent 不存在 | 否 |
| `AGENT_OFFLINE` | Agent 离线 | 是 |
| `AGENT_BUSY` | Agent 忙碌 | 是 |
| `TASK_INVALID` | 任务格式错误 | 否 |
| `TASK_REJECTED` | 任务被拒绝 | 否 |
| `TASK_TIMEOUT` | 任务超时 | 是 |
| `TASK_FAILED` | 任务执行失败 | 视情况 |
| `UNAUTHORIZED` | 未授权 | 否 |
| `RATE_LIMITED` | 请求过多 | 是 |

---

## 8. Agent 身份

### 8.1 Agent ID

```
格式: {agent_name}@{domain}

示例:
  booking-agent@example.com
  coder-agent@company.local
  translator-agent@team.org
```

### 8.2 去中心化发现

除了 Registry，还支持 `.well-known/agent.json`：

```
GET https://example.com/.well-known/agent.json

响应:
{
  "agent_id": "booking-agent@example.com",
  "name": "Booking Agent",
  "endpoint": "https://example.com/acp/agent",
  "capabilities": [...],
  "auth": {
    "type": "bearer"
  }
}
```

---

## 9. 扩展机制

ACP v0.1 只定义核心协议，其他功能通过扩展实现：

| 扩展 | 说明 | 状态 |
|------|------|------|
| `acp.payment` | 支付功能 | 计划中 |
| `acp.streaming` | 流式输出 | 计划中 |
| `acp.files` | 文件传输 | 计划中 |
| `acp.memory` | 记忆共享 | 计划中 |
| `acp.auth` | 高级认证 | 计划中 |

---

## 10. 示例

### 10.1 完整流程

```
1. Agent 注册
   Agent A → Registry: register
   Registry → Agent A: ok

2. 发现 Agent
   Agent B → Registry: discover (capability: booking)
   Registry → Agent B: [Agent A]

3. 发送任务
   Agent B → Agent A: send_task (book hotel)
   Agent A → Agent B: ok (accepted)

4. 查询状态
   Agent B → Agent A: get_status (task_id)
   Agent A → Agent B: completed (result)

5. 任务完成
```

### 10.2 Python 示例

```python
import requests

# 注册
requests.post("http://registry:8767/acp/register", json={
    "action": "register",
    "agent": {
        "agent_id": "booking-agent@example.com",
        "name": "Booking Agent",
        "endpoint": "http://localhost:8080/acp/agent",
        "capabilities": [{"name": "booking.hotel"}]
    }
})

# 发送任务
response = requests.post("http://localhost:8080/acp/task", json={
    "action": "send_task",
    "task": {
        "task_id": "task-001",
        "type": "booking.hotel",
        "input": {"city": "上海", "check_in": "2026-05-15"}
    }
})

# 查询状态
status = requests.get("http://localhost:8080/acp/task/task-001")
print(status.json())
```

---

## 11. 变更记录

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| 0.1.0-draft | 2026-05-01 | 初始草案，4 个核心动作 |

---

## 12. 参考资料

- [A2A Protocol](https://a2a-protocol.org/) - Agent-to-Agent 通信标准
- [MCP](https://modelcontextprotocol.io/) - 模型上下文协议
- [HTTP/1.1](https://tools.ietf.org/html/rfc2616) - 超文本传输协议
- [JSON-RPC 2.0](https://www.jsonrpc.org/specification) - JSON 远程过程调用

---

<p align="center">
  <strong>📝 RFC-001: ACP v0.1.0-draft</strong><br>
  <em>轻量级 Agent 通信协议</em>
</p>
