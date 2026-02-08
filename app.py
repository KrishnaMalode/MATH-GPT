import streamlit as st
from langchain_groq import ChatGroq

st.title("🧮 Math Solver")

# Get API key from secrets
api_key = st.secrets["GROQ_API_KEY"]

# Create LLM with SIMPLEST config
llm = ChatGroq(api_key=api_key)

# Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question := st.chat_input("Ask math question"):
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)
    
    with st.chat_message("assistant"):
        answer = llm.invoke(question).content
        st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
