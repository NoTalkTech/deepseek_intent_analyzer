# analyzer.py

import requests
import json
import re
from config import DEEPSEEK_API_KEY, DEEPSEEK_ENDPOINT, MODEL

SYSTEM_PROMPT = """
你是一个专业的数据仓库问答助手，具备逻辑推理、结构化分析和联网搜索能力。

请根据用户输入进行如下结构化输出。系统可能提供 search_info 字段，表示联网搜索摘要，请合理引用。

输出格式为：
{
  "summary": "...",
  "problem": "...",
  "intent": "...",
  "intent_class": "...",
  "suggestion": "...",
  "references": ["..."]
}
"""

def web_search(query, top_n=3):
    print(f"开始联网搜索: {query}")
    url = f"https://ddg-api.herokuapp.com/search?q={query}"
    try:
        resp = requests.get(url, timeout=5)
        results = resp.json().get("results", [])[:top_n]

        merged_snippets = []
        references = []

        for r in results:
            merged_snippets.append(r.get("snippet", ""))
            references.append({
                "title": r.get("title", ""),
                "snippet": r.get("snippet", ""),
                "url": r.get("link", "")
            })
        print(f"搜索结果: {merged_snippets}")
        search_summary = summarize_snippets(merged_snippets)
        print(f"联网搜索摘要: {search_summary}")
        return search_summary, references
    except Exception as e:
        return "", []

def summarize_snippets(snippets, original_question):
    merged_text = "\n".join(snippets)
    summary_prompt = f"""
你是一个内容摘要助手。请根据用户提出的问题，从以下网页摘要中提取有用信息，生成简洁的总结内容。
用户问题: {original_question}

网页摘要内容:
{merged_text}

请以 2~3 句话概括出与问题最相关的核心信息。
"""
    
    try:
        print(f"开始生成摘要: {summary_prompt}")
        summary = call_deepseek(summary_prompt, "你是一个专业的信息摘要助手。", 0.3)
        return summary.strip()
    except Exception as e:
        print(f"摘要失败：{e}")
        return "（摘要生成失败）"

def analyze_question(question, top_n=3):
    print(f"开始分析问题: {question}")
    search_summary, references = web_search(question, top_n)
    full_prompt = f"{question}\n\nsearch_info:\n{search_summary}"
    content = call_deepseek(full_prompt, SYSTEM_PROMPT, 0.3)
    try:
        json_str = re.search(r"\{[\s\S]+\}", content).group(0)
        parsed = json.loads(json_str)
        parsed.update({
            "question": question,
            "search_summary": search_summary,
            "references": references
        })
        return parsed, content, search_summary, references
    except Exception:
        return {
            "error": "无法解析模型输出",
            "raw_output": content
        }, content, search_summary, references
    
def call_deepseek(user_prompt: str, sys_prompt: str = SYSTEM_PROMPT, temperature: float = 0.3):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature
    }
    try:
        response = requests.post(DEEPSEEK_ENDPOINT, headers=headers, json=payload, timeout=150)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        return content
    except Exception as e:
        print(f"[DeepSeek调用失败] {e}")
        return "（模型调用失败）"