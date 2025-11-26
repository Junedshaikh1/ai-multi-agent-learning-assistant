import streamlit as st
import google.generativeai as genai
import os
import time

# -------------------------
# GEMINI CONFIG
# -------------------------
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_ID = "models/gemini-2.5-flash"

if not API_KEY:
    st.error("❌ API Key not found! Set $env:GEMINI_API_KEY first.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_ID)

# -------------------------
# CSS THEMING (SWAG LEVEL)
# -------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
}

/* Gradient Header */
.gradient-title {
    font-size: 42px;
    font-weight: 700;
    background: linear-gradient(90deg, #7A00FF, #00E5FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Animated Background */
.stApp {
    background: linear-gradient(-45deg, #0B0F19, #151B2D, #0E1628, #0D1020);
    background-size: 400% 400%;
    animation: gradientBG 20s ease infinite;
}
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Chat Bubbles */
.chat-bubble {
    background-color: #1F2436;
    padding: 15px;
    border-radius: 12px;
    border-left: 5px solid #7A00FF;
    margin-bottom: 15px;
}

/* Card UI */
.card {
    background-color: #1A1F2E;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #2C3245;
    margin-bottom: 20px;
}

/* Custom Button */
.stButton button {
    background: linear-gradient(90deg, #7A00FF, #00D1FF);
    color: white;
    padding: 12px 20px;
    border-radius: 12px;
    border: none;
    font-size: 18px;
    transition: 0.3s;
}
.stButton button:hover {
    transform: scale(1.03);
}

</style>
""",
unsafe_allow_html=True)

# -------------------------
# CLEAN TEXT OUTPUT
# -------------------------
def clean_output(raw):
    cleaned = (
        raw.replace("```json", "")
           .replace("```python", "")
           .replace("```", "")
           .replace("json", "")
           .replace("python", "")
           .strip()
    )
    return cleaned

# -------------------------
# AGENT FUNCTIONS
# -------------------------
def diagnosis_agent(user_text):
    prompt = f"""
Extract weak topics from:

{user_text}

Return a python dict:
{{
  "weak_topics": [...],
  "strengths": [...]
}}
"""
    t0 = time.time()
    result = model.generate_content(prompt)
    out = clean_output(result.text)
    try:
        data = eval(out)
    except:
        data = {"weak_topics": [], "strengths": []}
    return data, round(time.time()-t0,2)

def teaching_agent(weak):
    if not weak:
        return "No weak topics found.",0
    prompt = f"""
Explain these topics simply:

{weak}

Include:
- Explanation
- Analogy
- Python example
- 1 MCQ with answer
"""
    t0=time.time()
    res=model.generate_content(prompt)
    return res.text, round(time.time()-t0,2)

def plan_agent(diagnosis):
    t0=time.time()
    prompt=f"Create a 7-day study plan: {diagnosis}"
    res=model.generate_content(prompt)
    return res.text, round(time.time()-t0,2)

def reflection_agent(plan, weak):
    t0=time.time()
    prompt=f"""
Review this plan and provide:
- 3 improvements
- 3 motivation tips
- Score prediction based on weak topics {weak}
"""
    res=model.generate_content(prompt)
    return res.text, round(time.time()-t0,2)

# -------------------------
# SIDEBAR SWAG
# -------------------------
st.sidebar.title("⚡ Agent Controls")
st.sidebar.info("Adjust settings & view agent stats.")

st.sidebar.subheader("Model Used")
st.sidebar.success("Gemini 2.5 Flash")

st.sidebar.write("Made by **Juned Shaikh** 👑")

# -------------------------
# MAIN UI
# -------------------------
st.markdown("<h1 class='gradient-title'>🎓 AI Multi-Agent Learning Assistant</h1>", unsafe_allow_html=True)

user_input = st.text_area("✍️ Enter your weak topics, marks, or message:", height=130)

if st.button("🚀 Run Multi-Agent System"):
    
    with st.spinner("🔍 Running Diagnosis Agent..."):
        diagnosis, t1 = diagnosis_agent(user_input)

    with st.spinner("📘 Teaching Agent..."):
        teaching, t2 = teaching_agent(diagnosis["weak_topics"])

    with st.spinner("🗓️ Creating Study Plan..."):
        plan, t3 = plan_agent(diagnosis)

    with st.spinner("🔄 Reflection Agent..."):
        reflection, t4 = reflection_agent(plan, diagnosis["weak_topics"])

    st.success("✨ All Agents Completed!")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🧠 Diagnosis",
        "📘 Teaching",
        "🗓️ Study Plan",
        "💬 Reflection"
    ])

    with tab1:
        st.markdown("<div class='card'><h3>Weak Topics Identified</h3></div>", unsafe_allow_html=True)
        st.json(diagnosis)
        st.caption(f"⏱ Time: {t1}s")

    with tab2:
        st.markdown("<div class='chat-bubble'>" + teaching + "</div>", unsafe_allow_html=True)
        st.caption(f"⏱ Time: {t2}s")

    with tab3:
        st.markdown("<div class='chat-bubble'>" + plan + "</div>", unsafe_allow_html=True)
        st.caption(f"⏱ Time: {t3}s")

    with tab4:
        st.markdown("<div class='chat-bubble'>" + reflection + "</div>", unsafe_allow_html=True)
        st.caption(f"⏱ Time: {t4}s")
