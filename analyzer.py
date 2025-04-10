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

def web_search(query):
    url = f"https://ddg-api.herokuapp.com/search?q={query}"
    try:
        resp = requests.get(url, timeout=5)
        results = resp.json().get("results", [])
        summaries = [f"{r['title']} - {r['snippet']}" for r in results[:3]]
        return "\n".join(summaries)
    except Exception:
        return ""

def analyze_question(question, search_info=""):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    full_prompt = f"{question}\n\nsearch_info:\n{search_info}" if search_info else question
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(DEEPSEEK_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    content = result["choices"][0]["message"]["content"]

    try:
        json_str = re.search(r"\{[\s\S]+\}", content).group(0)
        parsed = json.loads(json_str)
        parsed["question"] = question
        parsed["search_info"] = search_info
        return parsed, content
    except Exception:
        return {
            "error": "无法解析输出",
            "raw_output": content
        }, content