import streamlit as st
from langchain_groq import ChatGroq
import os

st.title("🧮 Math Solver")
st.info("💡 Type a math question below!")

# Get API key safely
groq_api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
if not groq_api_key:
    st.error("❌ Add GROQ_API_KEY in Settings → Secrets")
    st.stop()

st.success("✅ API Key loaded!")

# Test connection first
if "llm" not in st.session_state:
    try:
        st.session_state.llm = ChatGroq(
            model="llama-3.2-1b-preview",  # ✅ WORKING MODEL
            api_key=groq_api_key,
            temperature=0.1
        )
        st.success("🤖 Groq connected!")
    except Exception as e:
        st.error(f"❌ Groq connection failed: {str(e)}")
        st.stop()

llm = st.session_state.llm

# Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask math question..."):
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Calculating..."):
                try:
                    response = llm.invoke(prompt)
                    answer = response.content
                except Exception as e:
                    answer = f"Error: {str(e)}"
            
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
