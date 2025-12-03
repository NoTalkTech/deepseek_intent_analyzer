#!/bin/bash
# 快速启动脚本

set -e

# 使用 uv 运行 streamlit
echo "🚀 启动 DeepSeek 意图分析器..."
uv run streamlit run app.py

