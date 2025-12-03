# DeepSeek 意图分析器

数据仓库意图识别 & 联网搜索助手，使用 DeepSeek API 和 Streamlit 构建。

## ⚡️ 快速开始

```bash
# 1. 安装 uv（如果还没有）
brew install uv

# 2. 安装依赖
uv sync

# 3. 设置 API Key
export DEEPSEEK_API_KEY="your-api-key-here"

# 4. 启动应用
./run.sh
```

就这么简单！🚀

## 📖 文档

- **[QUICKSTART.md](QUICKSTART.md)** - 快速开始和常见问题
- **[CHEATSHEET.md](CHEATSHEET.md)** - 命令速查表
- **[.cursorrules](.cursorrules)** - 项目开发规则

## 💡 功能特性

- ✅ DeepSeek API 意图分析
- ✅ 联网搜索集成
- ✅ 简洁的 Streamlit Web 界面
- ✅ 使用 uv 超快速依赖管理

## 📦 依赖管理

```bash
# 添加/删除依赖
uv add package-name
uv remove package-name

# 更新依赖
uv lock --upgrade && uv sync

# 查看已安装的包
uv pip list
```

## 🎨 代码质量

```bash
# 格式化代码
uv run ruff format .

# 检查代码
uv run ruff check .

# 自动修复问题
uv run ruff check --fix .
```

> 💡 **更多命令**: 查看 [CHEATSHEET.md](CHEATSHEET.md)

## 🛠️ 开发环境

### VS Code 集成

项目已配置 `.vscode/` 设置：
- ✅ 自动识别 `.venv` 虚拟环境
- ✅ 保存时自动格式化（Ruff）
- ✅ 按 F5 可直接调试 Streamlit 应用

### 技术栈

- **Python**: 3.11
- **包管理**: [uv](https://github.com/astral-sh/uv) - 比 pip 快 10-100 倍
- **Web 框架**: Streamlit
- **代码格式化**: Ruff
- **AI 模型**: DeepSeek API

## 📁 项目结构

```
deepseek_intent_analyzer/
├── 📱 核心文件
│   ├── app.py              # Streamlit 主应用
│   ├── analyzer.py         # 分析逻辑
│   └── config.py           # 配置管理
│
├── 🔧 配置
│   ├── pyproject.toml      # 项目配置和依赖
│   ├── uv.lock             # 依赖锁文件
│   └── .python-version     # Python 3.11
│
├── 📚 文档
│   ├── README.md           # 本文件
│   ├── QUICKSTART.md       # 快速开始
│   └── CHEATSHEET.md       # 命令速查
│
├── 🚀 脚本
│   └── run.sh              # 快速启动
│
└── 📝 其他
    ├── .vscode/            # VS Code 配置
    ├── .cursorrules        # Cursor 规则
    ├── env.example         # 环境变量模板
    └── examples/           # 示例文件
```

## 🤔 为什么选择 uv？

- ⚡️ **超快速** - 比 pip 快 10-100 倍
- 🔒 **可靠** - 自动生成锁文件，确保依赖一致
- 🎯 **简单** - 一个工具管理所有事情
- 🐍 **现代** - 符合 Python 社区最新标准

## 📝 许可证

查看 [LICENSE](LICENSE) 文件了解详情。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**💡 提示**: 
- 首次使用？查看 [QUICKSTART.md](QUICKSTART.md)
- 需要命令参考？查看 [CHEATSHEET.md](CHEATSHEET.md)
- 开发问题？查看 [.cursorrules](.cursorrules)
