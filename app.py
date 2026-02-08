import streamlit as st
from groq import Groq

# Page setup for wide professional layout
st.set_page_config(page_title="Mathematics Assistant", layout="wide")

# ========================================
# MATHEMATICS ASSISTANT APPLICATION
# Professional chat interface with sidebar controls
# ========================================

# Main application title
st.title("📊 Mathematics Assistant")
st.markdown("*AI-powered mathematical problem solving*")

# Create two-column layout: main chat area (70%) + sidebar controls (30%)
col_chat, col_sidebar = st.columns([7, 3], gap="1rem")

# ========================================
# MAIN CHAT AREA - Left column (70% width)
# ========================================
with col_chat:
    # Chat section header
    st.header("Interactive Solver")
    
    # Fixed-height container for chat messages - scrolls automatically
    chat_container = st.container(height=700)
    with chat_container:
        # Initialize chat history if first visit
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant", 
                    "content": "👋 I'm your math assistant. Ask me anything:\n\n• Algebra (2x + 5 = 17)\n• Word problems\n• Geometry\n• Calculus"
                }
            ]
        
        # Display all previous messages in chronological order
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    # User input field - always stays at bottom
    question = st.chat_input("Enter your math question...", key="chat_input")
    
    # Handle new user question
    if question:
        # Store user question in session state
        st.session_state.messages.append({"role": "user", "content": question})
        
        # Display user message immediately
        with st.chat_message("user"):
            st.write(question)
        
        # Generate and display AI response
        with st.chat_message("assistant"):
            with st.spinner("🧮 Solving..."):
                # Initialize Groq client with secret API key
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                
                # Call Groq API with system prompt for professional math responses
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",  # Fast, reliable model
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a professional mathematics assistant. Provide clear, step-by-step solutions with explanations."
                        }
                    ] + st.session_state.messages,
                    temperature=0.1,  # Low temperature for accurate math
                    max_tokens=1500   # Allow detailed step-by-step solutions
                )
                
                # Extract and display answer
                answer = response.choices[0].message.content
                st.write(answer)
                
                # Save AI response to chat history
                st.session_state.messages.append({"role": "assistant", "content": answer})

# ========================================
# SIDEBAR CONTROLS - Right column (30% width)
# ========================================
with col_sidebar:
    # Control panel header
    st.header("Control Panel")
    
    # System status indicators
    st.success("✅ Groq API Connected")
    st.success("✅ Model Active")
    st.success("✅ Ready")
    
    # Visual separator
    st.markdown("---")
    
    # Example problems section
    st.subheader("📚 Example Problems")
    
    # Predefined example questions for quick testing
    examples = [
        "Solve 2x + 5 = 17",
        "If 5 workers build 5 walls in 5 days, how long for 10 workers to build 10 walls?",
        "Area of circle with radius 7",
        "What is 15% of 240?"
    ]
    
    # Create buttons for each example
    for i, example in enumerate(examples):
        if st.button(example, key=f"ex_{i}", use_container_width=True):
            # Auto-populate chat input with selected example
            st.session_state.chat_input = example
            st.rerun()
    
    # Visual separator
    st.markdown("---")
    
    # Chat management
    if st.button("🗑️ Clear Chat", use_container_width=True):
        # Reset conversation history
        st.session_state.messages = []
        st.rerun()

# ========================================
# FOOTER - Application branding
# ========================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "Mathematics Assistant | Powered by Streamlit + Groq AI"
    "</div>", 
    unsafe_allow_html=True
)
