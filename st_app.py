import streamlit as st
from utils.function_calling import get_response
import os
from dotenv import load_dotenv

load_dotenv()

# Duke University color palette
DUKE_BLUE = "#00539B"  # Primary Duke Blue
DUKE_NAVY = "#012169"  # Duke Navy Blue
DUKE_WHITE = "#FFFFFF"
DUKE_GRAY = "#666666"

# Configure the page
st.set_page_config(
    page_title="Duke Student Advisor",
    page_icon="🔵",
    layout="wide",
)

# Apply Duke styling with CSS
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');

    body, h1 {{
        font-family: 'EB Garamond', serif !important;
    }}

    .main-title {{
        font-size: 4rem;
        font-weight: 100;
        margin: 0;
        text-align: center;
        letter-spacing: 0.02em;
    }}

    .stTextInput > label, .stTextArea > label {{
        color: {DUKE_WHITE};
        font-weight: bold;
    }}
    .stButton > button {{
        background-color: {DUKE_NAVY};
        color: {DUKE_WHITE};
        border-radius: 4px;
        border: none;
        padding: 0.5rem 1rem;
    }}
    .stButton > button {{
        background-color: {DUKE_BLUE};
    }}
    .stSidebar {{
        background-color: {DUKE_NAVY};
        color: {DUKE_WHITE};
    }}
    .stSidebar [data-testid="stMarkdownContainer"] p {{
        color: {DUKE_WHITE};
    }}
    .css-1d391kg {{
        background-color: {DUKE_NAVY};
    }}
    .sidebar .sidebar-content {{
        background-color: {DUKE_NAVY};
    }}
    .title-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 2rem;
        padding: 1rem;
        border-radius: 4px;
        color: {DUKE_NAVY};
    }}

    .input-container {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1rem 2rem;
        background-color: #ffffff;
        z-index: 100;
    }}

    .stChatInputContainer {{
        margin-bottom: 80px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []


# Title and header
st.markdown("""
    <div class="title-container" style="margin-top: -50px ;">
        <h1 class="main-title">Duke Student Advisor</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

# Sidebar - Duke University logo and instructions
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Duke_Athletics_logo.svg/1200px-Duke_Athletics_logo.svg.png", width=120)
    
    st.markdown("### How to Use")
    st.markdown("""Ask me anything about Duke University. I can help you with:

- MEM (Master of Engineering Management) program information
- Pratt School of Engineering programs
- Course information and details
                
Enter your OpenAI API key below to get started.""")
    
    # OpenAI API key input
    api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")

    if not api_key:
        try:
            api_key = os.getenv("OPENAI_API_KEY")
        except:
            st.warning("Please enter your OpenAI API key here or add it to the .env file to continue.")
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.success("Chat history cleared!")

# Display chat messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if api_key:
    # User input
    if user_input := st.chat_input("Enter your message here..."):
        
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(f"**User**: {user_input}")

        # Agent response handling
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_response(st.session_state.messages, api_key)
                if response.content:
                    st.markdown(response.content)
                    st.session_state.messages.append({"role": "assistant", "content": response.content})

else:
    st.error("Please enter your OpenAI API key here or add it to the .env file to continue.")