# app.py

import streamlit as st
from analyzer import analyze_question, web_search
import json

st.set_page_config(page_title="数据仓库问答分析器", layout="wide")

st.title("🧠 数据仓库意图识别 & 联网搜索助手")

st.markdown("输入一个数据相关的问题，我会分析你的意图、分类并给出建议，并结合联网搜索结果。")

input_question = st.text_area("✍️ 输入你的问题", height=100)

if st.button("🚀 开始分析", type="primary") and input_question.strip():
    with st.spinner("正在联网搜索 & 调用 DeepSeek 模型分析中..."):
        result, raw, search_summary, references = analyze_question(input_question, top_n=3)

    st.subheader("📌 模型结构化分析")
    if "error" in result:
        st.error(result["error"])
        st.text_area("原始模型输出", result["raw_output"], height=300)
    else:
        st.json(result)

        if search_summary:
            st.subheader("🔍 联网搜索摘要")
            st.text_area("Search Info", search_summary, height=200)

        with st.expander("📄 原始模型输出"):
            st.text_area("Raw Output", raw, height=300)

        st.download_button(
            label="💾 下载结果 JSON",
            data=json.dumps(result, ensure_ascii=False, indent=2),
            file_name="intent_analysis.json",
            mime="application/json"
        )