#!/bin/bash
# 快速启动脚本

set -e

# 检查 DEEPSEEK_API_KEY
if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo "⚠️  警告: 未设置 DEEPSEEK_API_KEY 环境变量"
    echo "请设置: export DEEPSEEK_API_KEY='your-key'"
    echo ""
fi

# 使用 uv 运行 streamlit
echo "🚀 启动 DeepSeek 意图分析器..."
uv run streamlit run app.py

