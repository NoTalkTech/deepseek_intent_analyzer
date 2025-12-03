import os

# 从环境变量读取 API Key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# 如果未设置 API Key，给出友好提示
if not DEEPSEEK_API_KEY:
    print("❌ 错误: 未设置 DEEPSEEK_API_KEY 环境变量")
    print("请设置环境变量:")
    print("  export DEEPSEEK_API_KEY='your-api-key-here'")
    print("\n或创建 .env 文件（不会提交到 Git）")
    # 注意：不要在这里退出，让应用启动时再处理

# 模型配置
DEEPSEEK_ENDPOINT = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"
