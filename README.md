<p align="center">
  <h1 align="center">🛒 Agent Hub</h1>
  <p align="center">
    <strong>构建下一代 Agent 互联网</strong><br>
    让 AI Agent 们自动搜索、比价、下单，人类只看结果
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

买家 Agent 自动搜索、比价、下单：

```
👤 用户: "我想买一台 MacBook Pro"
   ↓
🤖 买家 Agent → Hub → 找到 3 个卖家
   ↓
🤖 自动搜索商品信息
   ↓
📊 比较价格、评分、库存
   ↓
💡 智能推荐最优选择
   ↓
🛒 自动下单完成
   ↓
📦 订单确认，等待发货
```

### 运行效果

```
============================================================
🛒 Agent 购物协议 Demo
============================================================

👤 用户需求: 购买 MacBook Pro 14 M3 Pro

📋 步骤 1: 搜索商品
🔍 搜索 Apple Store...
🔍 搜索 极客数码...
🔍 搜索 全球购...

📊 步骤 2: 比较价格
排名   商品名                            价格           评分       卖家
--------------------------------------------------------------------------------
1    MacBook Pro 14 M3 Pro (海外版)  ¥12999      4.6      全球购数码
2    MacBook Pro 14 M3 Pro        ¥13999      4.7      极客数码旗舰店
3    MacBook Pro 14 M3 Pro        ¥14999      4.9      Apple Store 官方旗舰店
4    MacBook Pro 16 M3 Max        ¥27999      4.95     Apple Store 官方旗舰店

🤖 步骤 3: 智能推荐
💡 分析结果：
   🏆 性价比最高: MacBook Pro 14 M3 Pro (海外版) (¥12999, 评分 4.6)
   🚀 发货最快: MacBook Pro 14 M3 Pro (海外版) (库存 8 件)
   💰 价格最低: MacBook Pro 14 M3 Pro (海外版) (¥12999)

🛒 步骤 4: 自动下单
✅ 选择: MacBook Pro 14 M3 Pro (海外版)
📦 向 全球购数码 下单...

🎉 下单成功！
   订单号: ORD-20260501-003
   总金额: ¥12999
   预计送达: 2026-05-15
   物流单号: GL9876543210
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
│ 👤 用户 │               │ 🛒 卖家 │               │ 🏢 企业 │
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
pip install websockets
```

### 运行 Demo

```bash
python3 run_demo.py
```

---

## 🛒 购物场景详解

### 场景 1: 智能购物

```
用户: "我想买一台 MacBook Pro"
   ↓
买家 Agent:
   1. 搜索多个卖家（Apple Store、极客数码、全球购）
   2. 获取商品信息（价格、评分、库存、物流）
   3. 比较分析（性价比、发货速度、保修政策）
   4. 智能推荐最优选择
   5. 自动下单完成
```

### 场景 2: 批量采购

```
企业: "采购 100 台办公电脑"
   ↓
企业采购 Agent:
   1. 批量搜索供应商
   2. 获取批量报价
   3. 比较供应链稳定性
   4. 协商折扣
   5. 分批下单
```

### 场景 3: 跨境购物

```
用户: "买一台日本版 PS5"
   ↓
跨境购物 Agent:
   1. 搜索日本卖家
   2. 比较汇率和关税
   3. 计算总成本
   4. 选择最优物流
   5. 自动下单
```

---

## 🗺️ 路线图

### Phase 1: 基础协议 ✅
- [x] Agent URI 规范
- [x] Agent Hub 实现
- [x] 消息格式标准
- [x] 购物场景 Demo

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
