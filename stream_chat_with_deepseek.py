from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, MODEL
from openai import OpenAI

# 初始化 OpenAI 客户端（兼容 DeepSeek API）
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

# Turn 1
messages = [{"role": "user", "content": "9.11 and 9.8, which is greater?"}]
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    stream=True
)

reasoning_content = ""
content = ""

print("Turn 1 - 流式响应:")
for chunk in response:
    if chunk.choices[0].delta.reasoning_content:
        reasoning_content += chunk.choices[0].delta.reasoning_content
        print(chunk.choices[0].delta.reasoning_content, end="", flush=True)
    elif chunk.choices[0].delta.content:
        content += chunk.choices[0].delta.content
        print(chunk.choices[0].delta.content, end="", flush=True)

print("\n" + "="*60)
print(f"Reasoning: {reasoning_content[:100]}..." if reasoning_content else "No reasoning")
print(f"Content: {content}")

# Turn 2
print("\n" + "="*60)
print("Turn 2 - 流式响应:")
messages.append({"role": "assistant", "content": content})
messages.append({'role': 'user', 'content': "How many Rs are there in the word 'strawberry'?"})
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    stream=True
)

reasoning_content_2 = ""
content_2 = ""

for chunk in response:
    if chunk.choices[0].delta.reasoning_content:
        reasoning_content_2 += chunk.choices[0].delta.reasoning_content
        print(chunk.choices[0].delta.reasoning_content, end="", flush=True)
    elif chunk.choices[0].delta.content:
        content_2 += chunk.choices[0].delta.content
        print(chunk.choices[0].delta.content, end="", flush=True)

print("\n" + "="*60)
print(f"Turn 2 Content: {content_2}")