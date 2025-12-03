# 更新日志

## [未发布] - 2025-12-03

### 🔒 安全修复

#### 1. 移除硬编码的 API Key
- **文件**: `config.py`
- **问题**: API Key 硬编码在代码中，会被提交到 Git
- **修复**: 改为从环境变量读取，添加友好的错误提示
- **影响**: 防止 API Key 泄露

#### 2. 修复 URL 编码问题
- **文件**: `analyzer.py:36-38`
- **问题**: 搜索查询直接插入 URL，特殊字符未编码
- **修复**: 使用 `requests.get()` 的 `params` 参数自动编码
- **影响**: 
  - ✅ 支持空格、中文等特殊字符
  - ✅ 防止 `&`、`?` 等字符破坏 URL 结构
  - ✅ 提高搜索准确性

### 🐛 Bug 修复

#### 3. 修复 NoneType 错误和改进错误处理
- **文件**: `analyzer.py:110-136`
- **问题**: 
  - `re.search()` 可能返回 `None`，直接调用 `.group(0)` 会引发 `AttributeError`
  - 宽泛的 `except Exception` 掩盖了真实错误
- **修复**:
  - 在调用 `.group(0)` 前检查 `match` 是否为 `None`
  - 使用更精确的异常处理 (`ValueError`, `json.JSONDecodeError`)
  - 提供更清晰的错误信息
- **影响**: 
  - ✅ 防止因模型输出无 JSON 而崩溃
  - ✅ 更好的错误诊断和调试信息
  - ✅ 优雅的错误降级

### 📝 文档改进

#### 4. 更新环境变量说明
- **文件**: `env.example`
- **改进**: 添加详细的使用说明和 API Key 获取链接

### 📊 代码统计

- **总行数**: 197 行 Python 代码
  - `analyzer.py`: 143 行
  - `app.py`: 38 行
  - `config.py`: 16 行
- **代码质量**: ✅ All checks passed (Ruff)

### ⚠️ 破坏性变更

**需要设置环境变量**

之前可以使用默认的 API Key（不安全），现在必须设置环境变量：

```bash
export DEEPSEEK_API_KEY="your-api-key-here"
```

或创建 `.env` 文件（推荐）。

---

## 如何使用

### 设置 API Key

**方法 1: 环境变量**
```bash
export DEEPSEEK_API_KEY="your-api-key-here"
./run.sh
```

**方法 2: .env 文件（推荐）**
```bash
cp env.example .env
# 编辑 .env 填入你的 API Key
./run.sh
```

### 验证修复

```bash
# 检查代码质量
uv run ruff check .

# 测试 URL 编码
uv run python3 -c "
from urllib.parse import urlencode
print(urlencode({'q': 'ClickHouse & Flink?'}))
"
```

