# DeepSeek 意图分析器

数据仓库意图识别 & 联网搜索助手，使用 DeepSeek API 和 Streamlit 构建。

## ⚡️ 快速开始

```bash
# 1. 安装 uv（如果还没有）
brew install uv

# 2. 安装依赖
uv sync

# 3. 配置 API Key（两种方式任选其一）

# 方式 1: 使用 .env 文件（推荐）
cat > .env << EOF
DEEPSEEK_API_KEY=your-api-key-here
EOF

# 方式 2: 使用环境变量
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

- ✅ **DeepSeek API 意图分析** - 智能理解用户问题
- ✅ **联网搜索集成** - 自动搜索相关信息
- ✅ **简洁的 Web 界面** - Streamlit 构建
- ✅ **超快速依赖管理** - uv 比 pip 快 10-100 倍
- ✅ **自动加载 .env** - 使用 python-dotenv
- ✅ **灵活配置** - 支持自定义 API Base URL 和模型

## ⚙️ 配置选项

### 环境变量

项目支持通过 `.env` 文件或环境变量配置：

```bash
# 必需
DEEPSEEK_API_KEY=your-api-key-here

# 可选（高级配置）
DEEPSEEK_BASE_URL=https://api.deepseek.com  # 自定义 API 地址
DEEPSEEK_MODEL=deepseek-chat                 # 自定义模型名称
```

### 配置优先级

1. **系统环境变量**（最高优先级）
2. **`.env` 文件**
3. **默认值**

## 📦 常用命令

```bash
# 依赖管理
uv add package-name          # 添加依赖
uv remove package-name       # 删除依赖
uv lock --upgrade && uv sync # 更新依赖

# 代码质量
uv run ruff format .         # 格式化代码
uv run ruff check .          # 检查代码
uv run ruff check --fix .    # 自动修复

# 查看信息
uv pip list                  # 已安装的包
```

> 💡 **更多命令**: 查看 [CHEATSHEET.md](CHEATSHEET.md)

## 🛠️ 开发环境

### VS Code 集成

项目已配置 `.vscode/` 设置：
- ✅ 自动识别 `.venv` 虚拟环境
- ✅ 保存时自动格式化（Ruff）
- ✅ 按 F5 可直接调试 Streamlit 应用

### 技术栈

| 类别 | 技术 | 说明 |
|------|------|------|
| **语言** | Python 3.11 | 现代 Python 特性 |
| **包管理** | [uv](https://github.com/astral-sh/uv) | 比 pip 快 10-100 倍 |
| **Web 框架** | Streamlit | 快速构建数据应用 |
| **代码质量** | Ruff | 超快的 Python linter |
| **AI 模型** | DeepSeek API | 强大的语言模型 |
| **环境管理** | python-dotenv | 自动加载 .env 文件 |

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
    ├── .env                # 环境变量（不提交）
    └── examples/           # 示例文件
```

## 🤔 为什么选择 uv？

| 特性 | pip | uv |
|------|-----|-----|
| **速度** | 慢 | ⚡️ 快 10-100 倍 |
| **依赖锁定** | requirements.txt | 🔒 uv.lock（自动） |
| **环境管理** | 手动 venv | 🎯 自动管理 .venv |
| **跨平台** | ✅ | ✅ |
| **标准兼容** | ✅ | ✅ PEP 标准 |

## 🔧 高级用法

### 使用代理或自定义 API

如果需要使用代理或兼容的 API 服务：

```bash
# .env 文件
DEEPSEEK_API_KEY=your-key
DEEPSEEK_BASE_URL=https://your-proxy.example.com
```

### 自定义模型

```bash
# .env 文件
DEEPSEEK_API_KEY=your-key
DEEPSEEK_MODEL=deepseek-chat-v2
```

## 📝 许可证

查看 [LICENSE](LICENSE) 文件了解详情。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 🆘 常见问题

### Q: 为什么配置了 .env 文件还不生效？

**A**: 项目已集成 `python-dotenv`，会自动加载。确保：
- 文件名是 `.env`（不是 `.env.txt`）
- 文件在项目根目录
- 格式正确：`DEEPSEEK_API_KEY=xxx`（无空格）

### Q: 如何验证配置是否正确？

**A**: 运行应用时会显示：
```bash
$ ./run.sh
✅ 已加载 .env 文件: /path/to/.env
🚀 启动 DeepSeek 意图分析器...
```

### Q: 支持哪些环境变量？

**A**: 
- `DEEPSEEK_API_KEY` - API 密钥（必需）
- `DEEPSEEK_BASE_URL` - API 地址（可选，默认官方 API）
- `DEEPSEEK_MODEL` - 模型名称（可选，默认 deepseek-chat）

---

**💡 提示**: 
- 首次使用？查看 [QUICKSTART.md](QUICKSTART.md)
- 需要命令参考？查看 [CHEATSHEET.md](CHEATSHEET.md)
- 开发问题？查看 [.cursorrules](.cursorrules)
