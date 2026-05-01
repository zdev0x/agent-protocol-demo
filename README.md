<p align="center">
  <h1 align="center">🤖 ACP - Agent Communication Protocol</h1>
  <p align="center">
    <strong>轻量级 Agent 通信协议</strong><br>
    为个人开发者和中小团队提供简单、可实现的 Agent 注册、发现和协作规范
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-0.1.0--draft-orange" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Transport-HTTP%2FWebSocket-green" alt="Transport">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>

---

## 💡 这是什么？

**ACP (Agent Communication Protocol)** 是一个轻量级 Agent 通信协议草案。

### 定位

```
✅ 个人开发者学习 Agent 通讯
✅ 私有化 Agent 系统内部通讯
✅ 中小规模 Agent 网络
✅ Agent 协议教学和研究
✅ 快速原型验证
```

### 不是什么

```
❌ 不是 A2A 的替代品
❌ 不是 MCP 的替代品
❌ 不是全球 Agent 互联网标准
❌ 不是企业级生产协议
```

### 与现有协议的关系

| 协议 | 定位 | 关系 |
|------|------|------|
| **MCP** | LLM ↔ 工具/数据 | 互补，ACP 不涉及工具调用 |
| **A2A** | Agent ↔ Agent 互操作 | ACP 是简化版/学习版 |
| **ACP** | Agent ↔ Agent 通讯 | 轻量级，易实现 |

---

## 🎯 核心设计

ACP v0.1 只定义 **4 个核心动作**：

```
1. register    - Agent 注册
2. discover    - 能力发现
3. send_task   - 发送任务
4. get_status  - 查询状态
```

### 任务状态机

```
created → accepted → running → completed
                    ↘ failed
                    ↘ cancelled
                    ↘ expired
```

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/zdev0x/agent-protocol-demo.git
cd agent-protocol-demo
pip install -r requirements.txt
```

### 运行 Demo

```bash
python3 run_demo.py
```

### 运行测试

```bash
python3 run_tests.py
```

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| [RFC-001](./RFC-001-agent-protocol.md) | 协议规范 v0.1 |
| [ARCHITECTURE](./docs/ARCHITECTURE.md) | 系统架构设计 |
| [VISION](./docs/VISION.md) | 项目愿景 |
| [API](./docs/API.md) | API 参考 |
| [CONTRIBUTING](./CONTRIBUTING.md) | 贡献指南 |
| [CHANGELOG](./CHANGELOG.md) | 更新日志 |

---

## 📁 项目结构

```
agent-protocol-demo/
├── agent.py              # Agent 基类
├── registry.py           # Agent 注册中心
├── run_demo.py           # 购物场景 Demo
├── run_tests.py          # 测试运行器
├── requirements.txt      # 依赖列表
├── RFC-001-agent-protocol.md  # 协议规范
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── tests/
    ├── test_agent.py
    └── test_registry.py
```

---

## 🛒 Demo 示例

买家 Agent 自动搜索、比价、下单：

```
👤 用户: "我想买一台 MacBook Pro"
   ↓
🤖 买家 Agent → Registry → 找到 3 个卖家
   ↓
📊 比较价格、评分、库存
   ↓
💡 智能推荐最优选择
   ↓
🛒 自动下单完成
```

---

## 🗺️ 路线图

### v0.1 (当前)
- [x] 4 个核心动作
- [x] 基础 Demo
- [x] 单元测试

### v0.2 (计划)
- [ ] 任务状态机完善
- [ ] 去中心化发现 (.well-known)
- [ ] 认证机制
- [ ] 错误处理完善

### v1.0 (未来)
- [ ] 扩展机制
- [ ] SDK (Python/JS)
- [ ] 更多传输协议
- [ ] 社区建设

---

## 🤝 参与贡献

请查看 [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## 📄 License

MIT License - 详见 [LICENSE](./LICENSE)

---

<p align="center">
  <strong>⭐ 如果觉得有用，请给个 Star 支持一下！</strong><br>
  <em>轻量级 Agent 通信协议</em>
</p>
