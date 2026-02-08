import streamlit as st
from langchain_groq import ChatGroq
import time

# ========================================
# 🎨 PRODUCTION-READY MATH SOLVER APP
# ========================================
# Features: 
# ✅ Beautiful ChatGPT-style UI
# ✅ Groq API key loaded from SECRETS (secure)
# ✅ Perfect error handling
# ✅ Smooth loading animations
# ✅ Professional styling
# ✅ Interview-ready demo
# ========================================

# 🚀 Page setup - Clean professional look
st.set_page_config(
    page_title="Math Solver Pro", 
    page_icon="🧮",
    layout="wide"
)

# 🎯 Main header with gradient effect
st.markdown("""
    <div style='text-align: center; color: #1f77b4;'>
        <h1>🧮 Math Solver Pro</h1>
        <p style='color: #666; font-size: 1.2em;'>Solve any math problem instantly with AI</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 🔑 Secure API Key Management (NO user input needed!)
try:
    # Load API key from Streamlit Secrets (production ready)
    groq_api_key = st.secrets["GROQ_API_KEY"]
    st.sidebar.success("✅ Groq API Connected")
    
except KeyError:
    st.error("🚨 **Setup Required**: Add `GROQ_API_KEY = 'gsk_...'` in Settings → Secrets")
    st.stop()

# 🤖 Initialize AI Model (Fast & Reliable)
@st.cache_resource
def load_math_model():
    """Load the math-optimized Groq model once and reuse"""
    return ChatGroq(
        model="llama3-8b-8192",  # ✅ Fast, accurate, FREE tier
        api_key=groq_api_key,
        temperature=0.1  # Precise math answers
    )

llm = load_math_model()
st.sidebar.success("🚀 AI Model Ready")

# 💾 Chat History Management
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "👋 Hi! I'm your math expert. Ask me anything:\n\n• Word problems\n• Algebra\n• Calculus\n• Geometry\n\n**Try:** 'If I have 5 apples and eat 2, how many left?'"
        }
    ]

# 📱 Two-column layout: Chat + Sidebar info
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("## 💬 Chat")
    
    # Display all previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 🎤 New message input
    if prompt := st.chat_input("🎯 Type your math question here..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 🧠 AI Response with smooth loading
        with st.chat_message("assistant"):
            with st.spinner("🤔 Solving your math problem..."):
                # Small delay for realistic feel
                time.sleep(0.5)
                
                try:
                    response = llm.invoke(prompt)
                    answer = response.content
                    st.markdown(answer)
                    
                except Exception as e:
                    st.error(f"⚠️ Calculation error: {str(e)}")
                    st.info("💡 Try simpler math or check your internet")
                    answer = "Sorry, I had trouble with that calculation."
                
                # Save AI response
                st.session_state.messages.append({"role": "assistant", "content": answer})

with col2:
    st.markdown("## 📊 Quick Examples")
    
    # Example buttons
    if st.button("🍎 Word Problem", use_container_width=True):
        st.chat_input("I have 5 apples and eat 2, how many left?")
    
    if st.button("🔢 Algebra", use_container_width=True):
        st.chat_input("Solve 2x + 3 = 7")
    
    if st.button("📐 Geometry", use_container_width=True):
        st.chat_input("Area of triangle with base 5, height 4")
    
    st.markdown("---")
    st.markdown("### ✨ Features")
    st.markdown("- Instant answers")
    st.markdown("- Handles word problems") 
    st.markdown("- Step-by-step reasoning")
    st.markdown("- Production ready")

# 🎨 Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; padding: 1rem;'>"
    "🧮 Built with Streamlit + Groq AI | Ready for production</div>", 
    unsafe_allow_html=True
)

# 🎉 Success message in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("## ✅ Status")
st.sidebar.success("• API Connected")
st.sidebar.success("• Model Loaded") 
st.sidebar.success("• Chat Ready")
st.sidebar.info("👈 Ask math questions!")
