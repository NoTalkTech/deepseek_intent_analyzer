import os

# 优先从环境变量读取
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-352ffde9de0447ee9c2415e183439e1e")

# 模型配置
DEEPSEEK_ENDPOINT = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"
