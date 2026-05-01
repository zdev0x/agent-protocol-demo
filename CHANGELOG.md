# Changelog

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2026-05-01

### 🎉 首次发布

#### ✨ 新功能

- **Agent 基类** (`agent.py`)
  - WebSocket 通讯支持
  - 标准化消息格式 (AgentMessage)
  - Agent URI 统一地址格式
  - 自动消息路由

- **Agent Registry** (`registry.py`)
  - Agent 注册服务
  - 能力搜索和发现
  - 心跳管理

- **购物场景 Demo** (`run_demo.py`)
  - 多卖家搜索
  - 价格比较
  - 智能推荐
  - 自动下单

#### 📚 文档

- **RFC-001** - Agent 通讯协议规范
- **ARCHITECTURE** - 系统架构设计
- **VISION** - 项目愿景和路线图
- **API** - API 参考文档
- **CONTRIBUTING** - 贡献指南

#### 🧪 测试

- AgentMessage 单元测试
- AgentRegistry 单元测试
- 测试运行器

#### 🛠️ 工具

- `.gitignore` - Git 忽略配置
- `requirements.txt` - 依赖列表
- `LICENSE` - MIT 许可证

---

## [未发布]

### 计划功能

- [ ] Web 界面
- [ ] 分布式 Registry
- [ ] 消息加密
- [ ] 支付系统
- [ ] SDK (Python/JS)
