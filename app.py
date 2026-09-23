import streamlit as st
import sys

sys.path.append("src")

from copilot import ask_copilot


st.set_page_config(
    page_title="AI Product Analytics Copilot",
    page_icon="📊",
    layout="wide"
)

st.title("AI Product Analytics Copilot")

st.write(
    "Ask a business question about your product analytics data."
)

question = st.text_input(
    "Business question",
    placeholder="Example: Why did conversion rate drop in August?"
)

if st.button("Analyze"):

    if not question:
        st.warning("Please enter a business question.")

    else:
        with st.spinner("Analyzing your data..."):

            try:
                result = ask_copilot(question)

                st.success("Analysis complete")

                st.write(result)

            except Exception as e:
                st.error(f"Error: {e}")
