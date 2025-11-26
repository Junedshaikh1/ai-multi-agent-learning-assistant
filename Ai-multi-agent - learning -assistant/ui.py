import streamlit as st
import google.generativeai as genai
from tools.rag import search_memory, store_memory

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-flash")

st.set_page_config(page_title="AI Learning Assistant", layout="wide")

st.title("AI Multi-Agent Learning Assistant")

st.write("Enter your weak topics, marks or difficulties:")

query = st.text_input("Your Input")

if st.button("Run Agents"):
    
    # Diagnosis Agent
    st.subheader("Diagnosis Agent")
    diag_prompt = f"""
    Identify weak topics from this input:
    {query}
    Give output as JSON with two fields: weak_topics, strengths.
    """
    diag_resp = model.generate_content(diag_prompt).text
    st.code(diag_resp)

    # Teaching Agent
    st.subheader("Teaching Agent")
    teach_prompt = f"Explain the following topics simply with examples: {query}"
    teach_resp = model.generate_content(teach_prompt).text
    st.write(teach_resp)

    # Study Planner Agent
    st.subheader("Study Planner Agent")
    plan_prompt = f"Create a 7-day study plan for: {query}"
    plan_resp = model.generate_content(plan_prompt).text
    st.write(plan_resp)

    # Reflection Agent
    st.subheader("Reflection Agent")
    ref_prompt = f"Give improvement advice for these weaknesses: {query}"
    ref_resp = model.generate_content(ref_prompt).text
    st.write(ref_resp)

    # Save memory
    store_memory(query)
