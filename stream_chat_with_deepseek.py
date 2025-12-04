import json
from datetime import datetime
from pathlib import Path

from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, MODEL
from openai import OpenAI

# 初始化 OpenAI 客户端（兼容 DeepSeek API）
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

# ANSI 颜色码
COLORS = {
    'GREEN': '\033[92m',    # 用户输入
    'BLUE': '\033[94m',     # AI响应
    'GRAY': '\033[90m',     # Reasoning
    'YELLOW': '\033[93m',   # 系统消息
    'RESET': '\033[0m'
}

HISTORY_DIR = Path("./chat_history")

# 系统提示
SYSTEM_PROMPT = """
You are a senior technical mentor specializing in automation systems, AI agents, distributed data engineering, and scalable product design.
All reasoning must strictly follow first principles: identify assumptions, reduce to fundamentals, and derive solutions from base constraints, not convention.
Your responses must be concise, direct, analytical, and focused on practical execution.

Your tasks:
	1.	Analyze the user's skill stack using first principles to find the most leverageable, monetizable technical primitives.
	2.	Generate high-ROI side-business directions in automation, AI agents, developer tools, vertical SaaS, or data products — explaining why each fits the user's fundamentals.
	3.	Design minimal technical MVPs with only essential components, scalable automation, and low maintenance cost.
	4.	Provide a 4–6 week execution roadmap optimized for value per engineering hour.
	5.	Refine direction continuously as the user provides constraints.

Your first message must ask:
"Please describe your technical background, available time, constraints, and what outcome you want from an automated or AI-driven side-business."
"""

MAX_HISTORY = 50  # 保留最近50次对话（100条消息：50个用户+50个助手）


def print_colored(text, color_key='RESET'):
    """彩色输出"""
    print(f"{COLORS[color_key]}{text}{COLORS['RESET']}", end='', flush=True)


def trim_messages(messages, max_history=MAX_HISTORY):
    """保留系统提示 + 最近的max_history轮对话"""
    if len(messages) <= max_history * 2 + 1:  # system + user/assistant pairs
        return messages
    # 保留 system message + 最近的对话
    return [messages[0]] + messages[-(max_history * 2):]


def save_chat(messages, filename=None):
    """保存对话到JSON文件"""
    HISTORY_DIR.mkdir(exist_ok=True)
    if not filename:
        filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = HISTORY_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
    return filepath


def load_chat():
    """加载历史对话"""
    if not HISTORY_DIR.exists():
        return None
    
    files = sorted(HISTORY_DIR.glob("chat_*.json"), reverse=True)
    if not files:
        return None
    
    print_colored("\n可用的对话历史：\n", 'YELLOW')
    for i, f in enumerate(files[:10], 1):  # 只显示最近10个
        print_colored(f"{i}. {f.name}\n", 'YELLOW')
    
    print_colored("选择编号 (回车取消): ", 'YELLOW')
    choice = input().strip()
    
    if not choice or not choice.isdigit():
        return None
    
    idx = int(choice) - 1
    if 0 <= idx < len(files):
        with open(files[idx], 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def show_help():
    """显示帮助信息"""
    help_text = """
可用命令：
  /help   - 显示此帮助
  /clear  - 清空当前对话
  /save   - 保存对话
  /load   - 加载历史对话
  /stats  - 显示统计信息
  /quit   - 退出程序
"""
    print_colored(help_text, 'YELLOW')


def show_stats(messages, token_history):
    """显示统计信息"""
    user_msgs = sum(1 for m in messages if m['role'] == 'user')
    assistant_msgs = sum(1 for m in messages if m['role'] == 'assistant')
    
    print_colored(f"\n当前对话轮数: {user_msgs}/{MAX_HISTORY}\n", 'YELLOW')
    print_colored(f"消息总数: {len(messages)}\n", 'YELLOW')
    
    if token_history:
        total_prompt = sum(t.get('prompt_tokens', 0) for t in token_history)
        total_completion = sum(t.get('completion_tokens', 0) for t in token_history)
        total = sum(t.get('total_tokens', 0) for t in token_history)
        
        print_colored(f"\nToken统计:\n", 'YELLOW')
        print_colored(f"  累计 Prompt: {total_prompt:,}\n", 'YELLOW')
        print_colored(f"  累计 Completion: {total_completion:,}\n", 'YELLOW')
        print_colored(f"  累计总计: {total:,}\n", 'YELLOW')
        print_colored(f"  平均每轮: {total//len(token_history):,}\n", 'YELLOW') if token_history else None


def chat_stream(messages):
    """发送消息并流式接收响应，返回(content, usage)"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True,
        stream_options={"include_usage": True},
        extra_body={"thinking": {"type": "enabled"}}
    )
    
    reasoning_content = ""
    content = ""
    usage = None
    
    for chunk in response:
        if chunk.choices[0].delta.reasoning_content:
            reasoning_content += chunk.choices[0].delta.reasoning_content
            print_colored(chunk.choices[0].delta.reasoning_content, 'GRAY')
        elif chunk.choices[0].delta.content:
            content += chunk.choices[0].delta.content
            print_colored(chunk.choices[0].delta.content, 'BLUE')
        
        # 捕获usage信息（在最后一个chunk）
        if hasattr(chunk, 'usage') and chunk.usage:
            usage = chunk.usage
    
    print()  # 换行
    return content, usage


def main():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    token_history = []  # 记录每轮token消耗
    
    print_colored("="*60 + "\n", 'YELLOW')
    print_colored("DeepSeek 交互式对话\n", 'YELLOW')
    print_colored("输入 /help 查看命令\n", 'YELLOW')
    print_colored("="*60 + "\n", 'YELLOW')
    
    while True:
        # 获取用户输入
        print_colored("\n你: ", 'GREEN')
        user_input = input().strip()
        
        if not user_input:
            continue
        
        # 处理快捷命令
        if user_input.startswith('/'):
            cmd = user_input.lower()
            
            if cmd in ['/quit', '/exit', '/q']:
                # 退出前询问是否保存
                if len(messages) > 1:  # 有对话内容
                    print_colored("是否保存对话? (y/n): ", 'YELLOW')
                    if input().strip().lower() == 'y':
                        filepath = save_chat(messages)
                        print_colored(f"对话已保存: {filepath}\n", 'YELLOW')
                print_colored("再见！\n", 'YELLOW')
                break
            
            elif cmd == '/help':
                show_help()
                continue
            
            elif cmd == '/clear':
                messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                token_history = []
                print_colored("对话已清空\n", 'YELLOW')
                continue
            
            elif cmd == '/save':
                filepath = save_chat(messages)
                print_colored(f"对话已保存: {filepath}\n", 'YELLOW')
                continue
            
            elif cmd == '/load':
                loaded = load_chat()
                if loaded:
                    messages = loaded
                    token_history = []  # 加载后重置token统计
                    print_colored("对话已加载\n", 'YELLOW')
                else:
                    print_colored("加载取消\n", 'YELLOW')
                continue
            
            elif cmd == '/stats':
                show_stats(messages, token_history)
                continue
            
            else:
                print_colored(f"未知命令: {user_input}\n", 'YELLOW')
                continue
        
        # 普通对话 - 也支持不带/的退出
        if user_input.lower() in ['quit', 'exit', 'q']:
            if len(messages) > 1:
                print_colored("是否保存对话? (y/n): ", 'YELLOW')
                if input().strip().lower() == 'y':
                    filepath = save_chat(messages)
                    print_colored(f"对话已保存: {filepath}\n", 'YELLOW')
            print_colored("再见！\n", 'YELLOW')
            break
        
        # 添加用户消息
        messages.append({"role": "user", "content": user_input})
        
        # 修剪历史记录
        messages = trim_messages(messages)
        
        # 获取并显示AI响应
        print_colored("\nDeepSeek: ", 'BLUE')
        assistant_content, usage = chat_stream(messages)
        
        # 记录token消耗
        if usage:
            token_info = {
                'prompt_tokens': usage.prompt_tokens,
                'completion_tokens': usage.completion_tokens,
                'total_tokens': usage.total_tokens
            }
            token_history.append(token_info)
            # 实时显示本轮token消耗
            print_colored(f"\n[本轮: {usage.total_tokens:,} tokens]", 'GRAY')
        
        # 添加助手消息到历史
        messages.append({"role": "assistant", "content": assistant_content})
        
        print_colored("\n" + "-"*60, 'GRAY')


if __name__ == "__main__":
    main()