# 命令速查表

## 🚀 启动应用

```bash
./run.sh
```

## 📦 依赖管理

```bash
# 初始化/同步
uv sync

# 添加/删除
uv add package-name
uv remove package-name

# 更新
uv lock --upgrade && uv sync

# 查看
uv pip list
```

## 🎨 代码质量

```bash
# 格式化
uv run ruff format .

# 检查
uv run ruff check .

# 自动修复
uv run ruff check --fix .
```

## 🧹 清理

```bash
# 清理 Python 缓存
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete

# 重置环境
rm -rf .venv uv.lock
uv sync
```

## 📝 导出依赖（兼容性）

```bash
uv pip freeze > requirements.txt
```

## 🔧 环境变量

```bash
# 设置 API Key
export DEEPSEEK_API_KEY="your-key"

# 或创建 .env 文件（需要额外支持）
cp env.example .env
# 编辑 .env
```

## 📊 项目信息

```bash
# Python 版本
cat .python-version

# 项目信息
cat pyproject.toml

# 锁定的依赖
cat uv.lock
```

