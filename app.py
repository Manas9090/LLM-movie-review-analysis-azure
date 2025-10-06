# OPENAI_API_KEY = <your-openai-key>
# LANGCHAIN_API_KEY = <your-langsmith-key>
# LANGCHAIN_PROJECT = movie-review-app
# LANGCHAIN_TRACING_V2 = true
#streamlit run app.py --server.port=$PORT --server.address=0.0.0.0


import os
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate 
from langchain_openai import ChatOpenAI
from langsmith import traceable

# --- Load environment variables from Azure WebApp ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "movie-review-app")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true")

# --- LLM setup ---
llm = ChatOpenAI(model="gpt-4", temperature=0.6, api_key=OPENAI_API_KEY)

# --- Prompt setup ---
prompt = ChatPromptTemplate.from_template(
    "You are a movie critic. Analyze this review and provide a detailed response:\n\n{review}"
)

@traceable  # LangSmith monitoring
def analyze_review(review: str) -> str:
    chain = prompt | llm
    return chain.invoke({"review": review}).content

# --- Streamlit UI ---
st.set_page_config(page_title="🎬 Movie Review Analyzer", layout="centered")
st.title("🎥 Movie Review Analyzer with LLM")
st.markdown("Enter a movie review below and get a deep analysis:")

review_input = st.text_area("✍️ Write your review here", height=200)

if st.button("🧠 Analyze Review"):
    if review_input.strip():
        with st.spinner("Analyzing..."):
            result = analyze_review(review_input)
        st.success("✅ Analysis Complete!")
        st.markdown("### 💡 LLM Feedback:")
        st.write(result)
    else:
        st.warning("⚠️ Please enter a review before analyzing.")
