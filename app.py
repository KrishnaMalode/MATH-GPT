import streamlit as st
from groq import Groq

st.title("🧮 Math Solver - API Test")

# API Key
api_key = st.secrets["GROQ_API_KEY"]

# TEST BUTTON - Click this FIRST
if st.button("🔑 **TEST API CONNECTION**", use_container_width=True):
    try:
        client = Groq(api_key=api_key)
        # Simple test call
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ 2026 working model
            messages=[{"role": "user", "content": "Say hello"}]
        )
        st.success("✅ **API WORKS!** Model: " + response.choices[0].message.content)
        st.balloons()
    except Exception as e:
        st.error(f"❌ **API FAILED**: {str(e)}")
        st.info("🔧 Fix: console.groq.com → new API key")

# Chat (only if test passes)
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question := st.chat_input("✅ API OK? Ask math..."):
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=st.session_state.messages + [{"role": "user", "content": question}],
        temperature=0.1
    )
    answer = response.choices[0].message.content
    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
