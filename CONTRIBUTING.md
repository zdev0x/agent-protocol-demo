# 🤝 贡献指南

感谢你对 Agent Hub 的关注！我们欢迎所有形式的贡献。

---

## 📋 目录

- [如何贡献](#如何贡献)
- [开发环境](#开发环境)
- [代码规范](#代码规范)
- [提交 PR](#提交-pr)
- [报告 Bug](#报告-bug)
- [提出功能建议](#提出功能建议)
- [社区规范](#社区规范)

---

## 如何贡献

### 代码贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 非代码贡献

- 📝 改进文档
- 🐛 报告 Bug
- 💡 提出新功能
- 🎨 设计改进
- 🌍 翻译工作
- 📢 社区推广

---

## 开发环境

### 环境要求

- Python 3.10+
- Node.js 18+ (可选，用于前端)
- Docker (可选，用于容器化)

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/zdev0x/agent-hub.git
cd agent-hub

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 运行测试
pytest

# 启动开发服务器
python run_demo.py
```

### 项目结构

```
agent-hub/
├── agent_protocol/          # 核心协议实现
│   ├── __init__.py
│   ├── agent.py             # Agent 基类
│   ├── hub.py               # Hub 服务
│   ├── message.py           # 消息格式
│   └── registry.py          # 注册中心
│
├── docs/                    # 文档
│   ├── ARCHITECTURE.md      # 架构设计
│   ├── VISION.md            # 项目愿景
│   └── API.md               # API 文档
│
├── tests/                   # 测试
│   ├── test_agent.py
│   ├── test_hub.py
│   └── test_message.py
│
├── examples/                # 示例
│   ├── basic/
│   ├── advanced/
│   └── integration/
│
├── RFC-001-agent-protocol.md # 协议规范
├── README.md                # 项目说明
├── CONTRIBUTING.md          # 贡献指南
├── LICENSE                  # 许可证
└── requirements.txt         # 依赖
```

---

## 代码规范

### Python 代码规范

1. 遵循 PEP 8
2. 使用类型注解
3. 编写文档字符串
4. 保持函数简短（<50行）
5. 使用有意义的变量名

```python
# 好的例子
async def register_agent(self, agent_info: AgentInfo) -> RegisterResult:
    """注册 Agent 到 Hub
    
    Args:
        agent_info: Agent 信息
        
    Returns:
        RegisterResult: 注册结果
        
    Raises:
        DuplicateAgentError: Agent URI 已存在
    """
    pass

# 不好的例子
async def reg(self, a):
    pass
```

### 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**类型 (type)**:

- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

**示例**:

```bash
git commit -m "feat(agent): 添加 Agent 心跳功能"
git commit -m "fix(hub): 修复注册中心内存泄漏"
git commit -m "docs: 更新 README 文档"
```

---

## 提交 PR

### PR 检查清单

- [ ] 代码遵循项目规范
- [ ] 添加了必要的测试
- [ ] 测试通过
- [ ] 更新了相关文档
- [ ] 提交信息符合规范
- [ ] 没有破坏性更改

### PR 模板

```markdown
## 描述

简要描述你的更改

## 类型

- [ ] Bug 修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 重构
- [ ] 其他

## 测试

描述你如何测试了你的更改

## 截图（如适用）

添加截图展示你的更改

## 相关 Issue

Closes #123
```

---

## 报告 Bug

### Bug 报告模板

```markdown
## Bug 描述

简要描述 Bug

## 复现步骤

1. 进入 '...'
2. 点击 '...'
3. 滚动到 '...'
4. 看到错误

## 期望行为

描述你期望的行为

## 实际行为

描述实际发生的行为

## 环境信息

- OS: [例如 macOS 13.0]
- Python: [例如 3.11.0]
- Agent Hub: [例如 1.0.0]

## 截图

如果适用，添加截图帮助解释问题

## 附加信息

任何其他有助于诊断的信息
```

---

## 提出功能建议

### 功能建议模板

```markdown
## 功能描述

简要描述你想要的功能

## 使用场景

描述这个功能的使用场景

## 期望行为

描述你期望的功能行为

## 替代方案

描述你考虑过的替代方案

## 附加信息

任何其他相关信息
```

---

## 社区规范

### 行为准则

- 尊重所有参与者
- 接受建设性批评
- 专注于对社区最有利的事情
- 对其他社区成员表示同理心

### 沟通渠道

- **GitHub Issues**: 报告 Bug、提出功能建议
- **GitHub Discussions**: 技术讨论、问答
- **Discord**: 实时交流、社区活动
- **Twitter**: 项目动态、行业资讯

---

## 认可贡献者

我们感谢所有贡献者！所有贡献者都会被添加到项目的 README 中。

### 贡献者等级

| 等级 | 要求 |
|------|------|
| 🌟 Contributor | 提交了 1-5 个 PR |
| ⭐ Contributor | 提交了 6-20 个 PR |
| 🏆 Contributor | 提交了 20+ 个 PR |
| 💎 Core Team | 核心团队成员 |

---

## 问题标签

| 标签 | 说明 |
|------|------|
| `good first issue` | 适合新手的问题 |
| `help wanted` | 需要帮助的问题 |
| `bug` | Bug 报告 |
| `enhancement` | 新功能 |
| `documentation` | 文档相关 |
| `question` | 问题咨询 |

---

## 发布流程

### 版本号规范

使用 [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH

MAJOR: 不兼容的 API 变更
MINOR: 向后兼容的功能性新增
PATCH: 向后兼容的问题修复
```

### 发布步骤

1. 更新 CHANGELOG.md
2. 更新版本号
3. 创建 Git tag
4. 发布到 PyPI
5. 更新文档

---

## 获取帮助

如果你有任何问题，可以通过以下方式获取帮助：

1. 查看文档
2. 搜索 GitHub Issues
3. 在 GitHub Discussions 提问
4. 加入 Discord 社区

---

<p align="center">
  <strong>感谢你的贡献！🎉</strong><br>
  <em>让我们一起构建下一代 Agent 互联网</em>
</p>
