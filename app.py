import streamlit as st
from groq import Groq

# Basic page setup
st.set_page_config(page_title="Math Assistant", page_icon="📊", layout="wide")

# Light styling polish
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 900px;
        }
        [data-testid="stChatMessage"] {
            border-radius: 12px;
        }
        .stButton button {
            border-radius: 8px;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Mathematics Assistant")
st.markdown("AI-powered math problem solver — algebra, word problems, percentages, and more.")
st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! Ask me math questions like 'solve 2x+3=7' or word problems."}
    ]

# For example buttons, since st.chat_input can't be set programmatically
if "example_question" not in st.session_state:
    st.session_state.example_question = None

# Sidebar - Simple controls
with st.sidebar:
    st.header("⚙️ Controls")
    st.success("✅ Connected")

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! Ask me math questions like 'solve 2x+3=7' or word problems."}
        ]
        st.rerun()

    st.markdown("---")
    st.markdown("**💡 Try an example:**")
    examples = ["2x + 5 = 17", "5 apples minus 2", "15% of 200"]
    for ex in examples:
        if st.button(ex, key=f"ex_{ex}"):
            st.session_state.example_question = ex
            st.rerun()

    st.markdown("---")
    st.caption("Powered by Llama 3.1 8B via Groq")

# DISPLAY ALL MESSAGES - Auto-scrolls naturally
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "📊"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# INPUT ALWAYS AT BOTTOM - ChatGPT style
question = st.chat_input("Type your math question...")

# If an example button was clicked, use that instead
if st.session_state.example_question:
    question = st.session_state.example_question
    st.session_state.example_question = None

if question:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(question)

    # AI response
    with st.chat_message("assistant", avatar="📊"):
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
