import os

# 优先从环境变量读取
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "your_deepseek_api_key_here")

# 模型配置
DEEPSEEK_ENDPOINT = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"