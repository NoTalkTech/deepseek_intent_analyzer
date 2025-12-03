# 快速开始指南

## 第一次使用

```bash
# 1. 安装 uv（如果还没有）
brew install uv

# 2. 安装依赖
uv sync

# 3. 设置 API Key
export DEEPSEEK_API_KEY="your-key-here"

# 4. 运行应用
./run.sh
# 或者: uv run streamlit run app.py
```

## 日常开发

```bash
# 运行应用
./run.sh

# 添加新依赖
uv add package-name

# 格式化代码
uv run ruff format .

# 检查代码
uv run ruff check .
```

## 常见问题

### Q: 如何更新依赖？
```bash
uv lock --upgrade && uv sync
```

### Q: 如何导出 requirements.txt？
```bash
uv pip freeze > requirements.txt
```

### Q: 如何在 VS Code 中调试？
按 F5，选择 "Streamlit: Run App"

### Q: 虚拟环境在哪？
`.venv/` 目录，由 uv 自动管理

### Q: 如何重置环境？
```bash
rm -rf .venv uv.lock
uv sync
```

## uv vs pip 对比

| 操作 | pip | uv |
|------|-----|-----|
| 安装包 | `pip install package` | `uv add package` |
| 创建环境 | `python -m venv .venv` | `uv sync` (自动) |
| 锁定依赖 | `pip freeze > requirements.txt` | `uv lock` (自动) |
| 安装依赖 | `pip install -r requirements.txt` | `uv sync` |
| 速度 | 慢 | **快 10-100 倍** |

## 项目结构

```
.
├── app.py              # Streamlit 主应用
├── analyzer.py         # 分析逻辑
├── config.py           # 配置
├── pyproject.toml      # 项目配置（核心）
├── uv.lock             # 依赖锁文件
├── .venv/              # 虚拟环境
├── run.sh              # 快速启动
├── env.example         # 环境变量示例
└── .vscode/            # VS Code 配置
    ├── settings.json
    └── launch.json
```

