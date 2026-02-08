import streamlit as st
from groq import Groq

st.title("🧮 Math Solver")

# Load API key
api_key = st.secrets["GROQ_API_KEY"]

# Direct Groq client (no LangChain bullshit)
client = Groq(api_key=api_key)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# New question
if question := st.chat_input("Ask math question"):
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=st.session_state.messages,
                temperature=0.1
            )
            answer = response.choices[0].message.content
        
        st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
