import streamlit as st
from langchain_groq import ChatGroq

# Simple title (no fancy config causing crashes)
st.title("🧮 Math Solver")

# Load API key safely
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("Add GROQ_API_KEY to Settings → Secrets")
    st.stop()

# Load model 
llm = ChatGroq(
    model="llama3-8b-8192", 
    api_key=api_key,
    temperature=0
)

# Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question := st.chat_input("Ask math question"):
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = llm.invoke(question).content
        st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
