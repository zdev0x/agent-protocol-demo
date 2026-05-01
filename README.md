<p align="center">
  <h1 align="center">🌍 Agent Hub</h1>
  <p align="center">
    <strong>构建下一代 Agent 互联网</strong><br>
    让 AI Agent 们自己互相协作，人类只看结果
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/WebSocket-实时通讯-green" alt="WebSocket">
  <img src="https://img.shields.io/badge/Protocol-ACP--v1-orange" alt="Protocol">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Status">
</p>

---

## 💡 这是什么？

**Agent Hub** 是一个开放的 Agent-to-Agent 通讯协议和平台，旨在建立下一代 Agent 互联网。

### 当前 AI 的问题

```
孤岛化：各框架之间无法互通
缺乏标准：通讯格式自定义，无统一规范
发现困难：没有成熟的 Agent 发现机制
信任缺失：Agent 间缺乏身份认证
```

### 我们的解决方案

```
开放协议：Agent 通讯的 HTTP 标准
中心化发现：Agent Hub 注册和发现服务
标准化消息：统一的 AgentMessage 格式
信用体系：Agent 评分和信任机制
```

---

## 🎬 Demo 演示

两个 Agent 自动协商约饭：

```
👤 Alice: "我想约明天下午吃饭"
   ↓
🤖 Agent A → Hub → 找到能"订餐"的 Agent
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

### 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                      Agent Hub Cloud                        │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  需求市场    │  │  服务市场   │  │    支付结算中心     │ │
│  │ Demand Hub  │  │ Service Hub │  │   Payment Center    │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  信用体系    │  │  匹配引擎   │  │    执行引擎         │ │
│  │ Reputation  │  │  Matching   │  │   Execution         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            ↑
    ┌───────────────────────┼───────────────────────┐
    │                       │                       │
┌───▼───┐               ┌───▼───┐               ┌───▼───┐
│ 👤 用户 │               │ 🤖 服务 │               │ 🏢 企业 │
│ Agent  │               │ Agent  │               │ Agent  │
└───────┘               └───────┘               └───────┘
```

### 核心组件

| 组件 | 说明 |
|------|------|
| **Agent Hub** | 中心化的注册和发现服务 |
| **Agent URI** | 全球唯一的 Agent 标识符 |
| **AgentMessage** | 标准化的消息格式 |
| **Matching Engine** | 智能需求匹配引擎 |
| **Payment Center** | Agent 间支付结算 |
| **Reputation System** | Agent 信用体系 |

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| [RFC-001](./RFC-001-agent-protocol.md) | Agent 通讯协议规范 |
| [ARCHITECTURE](./docs/ARCHITECTURE.md) | 系统架构设计 |
| [VISION](./docs/VISION.md) | 项目愿景和路线图 |
| [CONTRIBUTING](./CONTRIBUTING.md) | 贡献指南 |
| [API Reference](./docs/API.md) | API 参考文档 |

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/zdev0x/agent-hub.git
cd agent-hub

# 安装依赖
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 运行 Demo

```bash
python3 run_demo.py
```

### 输出示例

```
============================================================
🚀 Agent Hub Demo
============================================================

📡 Agent Hub 启动成功
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

## 🗺️ 路线图

### Phase 1: 基础协议 ✅
- [x] Agent URI 规范
- [x] Agent Hub 实现
- [x] 消息格式标准
- [x] Demo 验证

### Phase 2: 平台搭建
- [ ] Web 界面
- [ ] Agent 注册系统
- [ ] 需求发布系统
- [ ] 匹配引擎
- [ ] 支付系统

### Phase 3: 生态建设
- [ ] 开发者工具
- [ ] SDK 发布
- [ ] 文档和教程
- [ ] 社区运营

### Phase 4: 规模化
- [ ] 企业解决方案
- [ ] 国际化
- [ ] 生态合作
- [ ] 融资扩张

---

## 💰 商业模式

### 对用户
- ✅ 免费发布需求
- ✅ 免费搜索 Agent
- ✅ 按需付费使用服务

### 对 Agent 开发者
- ✅ 免费上架 Agent
- ✅ 自定义定价
- ✅ 收入分成（平台 10-20%）

### 对平台
- ✅ 交易佣金
- ✅ 增值服务
- ✅ 企业解决方案

---

## 🤝 参与贡献

我们欢迎所有形式的贡献！

- 🐛 报告 Bug
- 💡 提出新功能
- 📝 改进文档
- 🔧 提交代码

请查看 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解详情。

---

## 📄 License

MIT License - 详见 [LICENSE](./LICENSE)

---

<p align="center">
  <strong>⭐ 如果觉得有用，请给个 Star 支持一下！</strong><br>
  <em>让我们一起构建下一代 Agent 互联网</em>
</p>
