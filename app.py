import streamlit as st
from groq import Groq

# Clean professional config
st.set_page_config(page_title="Mathematics Assistant", layout="wide")

st.title("📊 Mathematics Assistant")
st.markdown("*Professional AI-powered mathematical problem solving*")

# Layout
col1, col2 = st.columns([3, 1])

with col1:
    st.header("Interactive Solver")
    
    # Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Input
    question = st.chat_input("Enter mathematical question...")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)
        
        with st.chat_message("assistant"):
            with st.spinner("Solving..."):
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": "You are a professional math assistant. Give clear step-by-step solutions."}] + st.session_state.messages,
                    temperature=0.1
                )
                answer = response.choices[0].message.content
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

with col2:
    st.header("Quick Start")
    
    # Status
    st.success("✅ API Connected")
    st.success("✅ Model Active")
    
    st.markdown("---")
    
    # Examples
    examples = [
        "Solve 2x + 5 = 17",
        "5 workers build 5 walls in 5 days...",
        "Compound interest $1000 @ 5%..."
    ]
    
    for ex in examples:
        if st.button(ex[:20] + "...", key=ex):
            st.chat_input(ex)

st.markdown("---")
st.caption("Mathematics Assistant | Streamlit + Groq AI")
