import streamlit as st
from groq import Groq

# Basic page setup
st.set_page_config(page_title="Math Assistant", layout="wide")

st.title("📊 Mathematics Assistant")
st.markdown("AI-powered math problem solver")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! Ask me math questions like 'solve 2x+3=7' or word problems."}
    ]

# DISPLAY ALL MESSAGES - Auto-scrolls naturally
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# INPUT ALWAYS AT BOTTOM - ChatGPT style
question = st.chat_input("Type your math question...")

if question:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    
    # AI response
    with st.chat_message("assistant"):
        with st.spinner("Solving..."):
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "system", "content": "You are a math expert. Give clear step-by-step answers."}] + st.session_state.messages,
                temperature=0.1
            )
            answer = response.choices[0].message.content
        
        st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

# Sidebar - Simple controls
with st.sidebar:
    st.header("Controls")
    st.success("✅ Connected")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("**Examples:**")
    examples = ["2x + 5 = 17", "5 apples minus 2", "15% of 200"]
    for ex in examples:
        if st.button(ex):
            st.session_state.chat_input = ex
            st.rerun()
