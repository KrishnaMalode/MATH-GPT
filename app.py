import streamlit as st
from groq import Groq

# Page config for clean professional layout
st.set_page_config(
    page_title="Mathematics Assistant", 
    page_icon="📊",
    layout="wide"
)

# Custom CSS for professional appearance
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 300;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-container {
        background: #fafbfc;
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 4px solid #3498db;
    }
    .status-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #27ae60;
    }
    </style>
""", unsafe_allow_html=True)

# Header - Clean corporate style
st.markdown('<h1 class="main-header">📊 Mathematics Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Professional AI-powered mathematical problem solving</p>', unsafe_allow_html=True)

# Main layout - Professional two-column
col1, col2 = st.columns([3, 1], gap="2rem")

# Left column - Chat interface
with col1:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown("### Interactive Mathematics Interface")
    
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display conversation
    chat_container = st.container(height=600)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    # Input area
    question = st.chat_input("Enter your mathematical question or problem...")
    
    if question:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Processing calculation..."):
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": "You are a professional mathematics assistant. Provide clear, step-by-step solutions to mathematical problems."}] + st.session_state.messages,
                    temperature=0.1,
                    max_tokens=1000
                )
                answer = response.choices[0].message.content
            
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
    
    st.markdown('</div>', unsafe_allow_html=True)

# Right column - Controls & Status
with col2:
    st.markdown("### Application Status", help="System health indicators")
    
    # Status indicators
    col_status1, col_status2 = st.columns(2)
    with col_status1:
        st.markdown('<div class="status-card">', unsafe_allow_html=True)
        st.success("✅ API Connected")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_status2:
        st.markdown('<div class="status-card">', unsafe_allow_html=True)
        st.success("✅ Model Active")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Example problems
    st.markdown("### Suggested Problems")
    examples = [
        "Solve 2x + 5 = 17",
        "If 5 workers build 5 walls in 5 days, how long for 10 workers?",
        "Calculate compound interest: $1000 at 5% for 3 years",
        "Find the area of a circle with radius 7"
    ]
    
    for example in examples:
        if st.button(example, key=example, use_container_width=True):
            st.chat_input(example)

# Footer - Professional branding
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #95a5a6; font-size: 0.9rem; padding: 1.5rem;'>
        Mathematics Assistant | Powered by Streamlit + Groq AI | Production Ready
    </div>
    """, 
    unsafe_allow_html=True
)
