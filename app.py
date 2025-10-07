import os
import openai
import streamlit as st

# --- Load OpenAI API key ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# --- Helper function to call OpenAI ---
def analyze_review(review: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional movie critic."},
                {"role": "user", "content": f"Analyze this review in detail and provide constructive feedback:\n\n{review}"}
            ],
            temperature=0.6,
            max_tokens=500
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error calling OpenAI API: {e}"

# --- Streamlit UI ---
st.set_page_config(page_title="Movie Review Analyzer", layout="centered")
st.title("Movie Review Analyzer with LLM")
st.markdown("Enter a movie review below and get a deep AI-powered analysis:")

review_input = st.text_area("Write your review here", height=200)

if st.button("Analyze Review"):
    if review_input.strip():
        if not OPENAI_API_KEY:
            st.error("OpenAI API key not set. Please configure the OPENAI_API_KEY environment variable.")
        else:
            with st.spinner("Analyzing..."):
                result = analyze_review(review_input)
            st.success("Analysis Complete!")
            st.markdown("### LLM Feedback:")
            st.write(result)
    else:
        st.warning("Please enter a review before analyzing.")
