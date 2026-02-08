import streamlit as st
from langchain_groq import ChatGroq

st.title("🧮 Math Problem Solver")
st.markdown("---")

# API Key
groq_api_key = st.secrets.get("GROQ_API_KEY", "")
if not groq_api_key:
    st.error("🚨 GROQ_API_KEY not found in Secrets. Add it in Settings.")
    st.stop()

# LLM
@st.cache_resource
def load_llm():
    return ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

llm = load_llm()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! Ask me any math question!"}
    ]

# Display chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a math question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Solving..."):
            response = llm.invoke(prompt)
        st.markdown(response.content)
        st.session_state.messages.append({"role": "assistant", "content": response.content})

