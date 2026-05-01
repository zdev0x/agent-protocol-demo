# 📚 API 参考文档

> Agent Hub API 详细说明

---

## 目录

- [Agent Hub API](#agent-hub-api)
- [Agent API](#agent-api)
- [WebSocket 协议](#websocket-协议)
- [消息格式](#消息格式)
- [错误码](#错误码)

---

## Agent Hub API

### 注册 Agent

**端点**: `POST /api/v1/agents/register`

**请求**:

```json
{
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
```

**响应**:

```json
{
  "status": "ok",
  "message": "已注册: agent://localhost:8765/alice/v1",
  "agent_id": "alice-8765",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 发现 Agent

**端点**: `POST /api/v1/agents/discover`

**请求**:

```json
{
  "query": {
    "capabilities": ["booking"],
    "min_reputation": 0.8,
    "max_latency": 1000,
    "limit": 10
  }
}
```

**响应**:

```json
{
  "status": "ok",
  "agents": [
    {
      "uri": "agent://localhost:8766/bob/v1",
      "name": "bob",
      "capabilities": ["booking", "scheduling"],
      "description": "旅行助手，擅长预订服务",
      "reputation": 0.95,
      "latency": 200,
      "endpoint": "ws://localhost:8766",
      "status": "active"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10
}
```

### 获取 Agent 详情

**端点**: `GET /api/v1/agents/{agent_uri}`

**响应**:

```json
{
  "status": "ok",
  "agent": {
    "uri": "agent://localhost:8766/bob/v1",
    "name": "bob",
    "capabilities": ["booking", "scheduling"],
    "description": "旅行助手，擅长预订服务",
    "reputation": 0.95,
    "total_tasks": 1234,
    "success_rate": 0.98,
    "avg_latency": 200,
    "created_at": "2026-01-01T00:00:00Z",
    "last_heartbeat": "2026-05-01T15:30:00Z"
  }
}
```

### 更新 Agent

**端点**: `PUT /api/v1/agents/{agent_uri}`

**请求**:

```json
{
  "capabilities": ["booking", "scheduling", "payment"],
  "description": "全能旅行助手",
  "metadata": {
    "version": "2.0.0"
  }
}
```

**响应**:

```json
{
  "status": "ok",
  "message": "Agent 已更新"
}
```

### 注销 Agent

**端点**: `DELETE /api/v1/agents/{agent_uri}`

**响应**:

```json
{
  "status": "ok",
  "message": "Agent 已注销"
}
```

### 心跳

**端点**: `POST /api/v1/agents/{agent_uri}/heartbeat`

**响应**:

```json
{
  "status": "ok",
  "ttl": 300,
  "next_heartbeat": "2026-05-01T15:35:00Z"
}
```

---

## Agent API

### 发送消息

**WebSocket**: `ws://agent-endpoint/send`

**请求**:

```json
{
  "action": "send",
  "message": {
    "id": "msg-a1b2c3d4",
    "version": "1.0",
    "type": "request",
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
      "priority": "normal"
    }
  }
}
```

**响应**:

```json
{
  "status": "ok",
  "message_id": "msg-a1b2c3d4",
  "timestamp": "2026-05-01T15:30:01Z"
}
```

### 接收消息

**WebSocket**: `ws://agent-endpoint/receive`

**响应**:

```json
{
  "action": "receive",
  "message": {
    "id": "msg-e5f6g7h8",
    "version": "1.0",
    "type": "response",
    "sender": {
      "uri": "agent://localhost:8766/bob/v1",
      "name": "bob"
    },
    "receiver": {
      "uri": "agent://localhost:8765/alice/v1",
      "name": "alice"
    },
    "payload": {
      "intent": "book_meeting.response",
      "data": {
        "accepted": true,
        "confirmed_time": "2026-05-02T14:00:00+08:00",
        "location": "上海人民广场海底捞 🍲"
      }
    },
    "metadata": {
      "timestamp": "2026-05-01T15:30:02Z",
      "reply_to": "msg-a1b2c3d4"
    }
  }
}
```

---

## WebSocket 协议

### 连接建立

```javascript
// 客户端连接
const ws = new WebSocket('ws://hub:8767');

// 连接成功
ws.onopen = () => {
  console.log('连接成功');
  
  // 发送认证
  ws.send(JSON.stringify({
    action: 'auth',
    token: 'your-token-here'
  }));
};

// 接收消息
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('收到消息:', data);
};

// 连接关闭
ws.onclose = () => {
  console.log('连接关闭');
};

// 错误处理
ws.onerror = (error) => {
  console.error('连接错误:', error);
};
```

### 心跳机制

```javascript
// 客户端心跳
setInterval(() => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({
      action: 'heartbeat'
    }));
  }
}, 30000); // 每30秒
```

### 重连机制

```javascript
function connectWithRetry(url, maxRetries = 3) {
  let retries = 0;
  
  function connect() {
    const ws = new WebSocket(url);
    
    ws.onopen = () => {
      console.log('连接成功');
      retries = 0;
    };
    
    ws.onclose = () => {
      if (retries < maxRetries) {
        retries++;
        console.log(`重连中 (${retries}/${maxRetries})...`);
        setTimeout(connect, 1000 * retries);
      }
    };
    
    return ws;
  }
  
  return connect();
}
```

---

## 消息格式

### AgentMessage

```json
{
  "id": "string",                    // 消息 ID (UUID)
  "version": "string",               // 协议版本
  "type": "string",                  // 消息类型
  "sender": {
    "uri": "string",                 // 发送者 URI
    "name": "string"                 // 发送者名称
  },
  "receiver": {
    "uri": "string",                 // 接收者 URI
    "name": "string"                 // 接收者名称
  },
  "payload": {},                     // 消息内容
  "metadata": {
    "timestamp": "string",           // ISO 8601 时间戳
    "ttl": "number",                 // 消息有效期 (秒)
    "priority": "string",            // 优先级
    "reply_to": "string|null",       // 回复的消息 ID
    "conversation_id": "string|null" // 会话 ID
  },
  "signature": {                     // 消息签名 (可选)
    "algorithm": "string",
    "value": "string",
    "signed_fields": ["string"]
  }
}
```

### 消息类型

| 类型 | 说明 | 需要响应 |
|------|------|----------|
| `request` | 请求消息 | 是 |
| `response` | 响应消息 | 否 |
| `notification` | 通知消息 | 否 |
| `error` | 错误消息 | 否 |

### 常用 Intent

**协作类**:

| Intent | 说明 |
|--------|------|
| `collaborate.request` | 请求协作 |
| `collaborate.accept` | 接受协作 |
| `collaborate.reject` | 拒绝协作 |
| `collaborate.complete` | 协作完成 |

**任务类**:

| Intent | 说明 |
|--------|------|
| `task.assign` | 分配任务 |
| `task.update` | 更新任务状态 |
| `task.complete` | 任务完成 |
| `task.cancel` | 取消任务 |

**支付类**:

| Intent | 说明 |
|--------|------|
| `payment.request` | 请求支付 |
| `payment.confirm` | 确认支付 |
| `payment.refund` | 退款 |

---

## 错误码

### HTTP 错误码

| 错误码 | 说明 |
|--------|------|
| 400 | 请求格式错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 408 | 请求超时 |
| 429 | 请求过多 |
| 500 | 服务器错误 |
| 503 | 服务不可用 |

### Agent 错误码

| 错误码 | 说明 |
|--------|------|
| `AGENT_NOT_FOUND` | Agent 不存在 |
| `AGENT_OFFLINE` | Agent 离线 |
| `AGENT_BUSY` | Agent 忙碌 |
| `AGENT_UNAUTHORIZED` | Agent 未授权 |
| `AGENT_RATE_LIMITED` | Agent 请求过多 |

### 消息错误码

| 错误码 | 说明 |
|--------|------|
| `MESSAGE_INVALID` | 消息格式错误 |
| `MESSAGE_EXPIRED` | 消息已过期 |
| `MESSAGE_TOO_LARGE` | 消息过大 |
| `MESSAGE_DUPLICATE` | 消息重复 |

### 错误响应格式

```json
{
  "status": "error",
  "error": {
    "code": "AGENT_NOT_FOUND",
    "message": "Agent not found",
    "details": {
      "agent_uri": "agent://localhost:8766/bob/v1"
    }
  },
  "timestamp": "2026-05-01T15:30:00Z"
}
```

---

## SDK 示例

### Python SDK

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

print(f"响应: {response}")
```

### JavaScript SDK

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

console.log('响应:', response);
```

### cURL 示例

```bash
# 注册 Agent
curl -X POST http://hub:8767/api/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{
    "uri": "agent://localhost:8765/alice/v1",
    "name": "alice",
    "capabilities": ["booking", "scheduling"],
    "endpoint": "ws://localhost:8765"
  }'

# 发现 Agent
curl -X POST http://hub:8767/api/v1/agents/discover \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "capabilities": ["booking"]
    }
  }'

# 获取 Agent 详情
curl http://hub:8767/api/v1/agents/agent://localhost:8766/bob/v1
```

---

## 速率限制

### 默认限制

| API | 限制 |
|-----|------|
| 注册 | 10 次/分钟 |
| 发现 | 100 次/分钟 |
| 发送消息 | 1000 次/分钟 |
| 心跳 | 1 次/30秒 |

### 响应头

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1620000000
```

---

<p align="center">
  <strong>📚 API 参考文档 v1.0</strong><br>
  <em>Agent Hub - 构建下一代 Agent 互联网</em>
</p>
