import streamlit as st
from langchain_groq import ChatGroq
import os

st.set_pageconfig(page_title="Math Solver", page_icon="🧮")
st.title("🧮 Math Problem Solver")

# API Key
groq_api_key = st.sidebar.text_input("Groq API Key", type="password")
if not groq_api_key:
    st.info("👈 Please add your Groq API key from console.groq.com")
    st.stop()

# LLM
llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a math question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm.invoke(prompt)
        st.markdown(response.content)
        st.session_state.messages.append({"role": "assistant", "content": response.content})
