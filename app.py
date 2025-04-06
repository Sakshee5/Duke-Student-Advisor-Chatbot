import streamlit as st
from openai import OpenAI
from datetime import datetime
import uuid
from streamlit_chat import message

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
    .stChatMessage {{
        background-color: {DUKE_BLUE};
        color: {DUKE_WHITE};
    }}
    footer {{
        visibility: hidden;
    }}
    #MainMenu {{visibility: hidden;}}
    .stActionButton {{
        display: none !important;
    }}
    .input-container {{
    margin-top: 2rem;
    }}
    .stChatInputContainer {{
        margin-bottom: 80px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

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
    st.markdown("""Ask me anything about Duke University. I'm here to help you with your questions and concerns about academics, housing, dining, and more.
                
Enter your OpenAI API key below to get started.""")
    
    # OpenAI API key input
    api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_id = str(uuid.uuid4())
        st.success("Chat history cleared!")

# Function to process messages
def process_message():
    user_message = st.session_state.user_input
    if not user_message.strip():  # Skip empty messages
        return

    # Add user message to history
    timestamp = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({
        "role": "user",
        "content": user_message,
        "timestamp": timestamp
    })
    
    # Clear the input field
    st.session_state.user_input = ""
    
    if api_key:
        try:
            # Initialize OpenAI client
            client = OpenAI(api_key=api_key)
            
            # Prepare the conversation history for the API
            conversation = [
                {"role": msg["role"], "content": msg["content"]} 
                for msg in st.session_state.messages 
                if msg["role"] in ["user", "assistant"]
            ]
            
            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=conversation,
            )
            
            # Extract the response
            ai_response = response.choices[0].message.content
            
            # Add assistant response to history
            timestamp = datetime.now().strftime("%I:%M %p")
            st.session_state.messages.append({
                "role": "assistant",
                "content": ai_response,
                "timestamp": timestamp
            })
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter your OpenAI API key in the sidebar.")

# Display chat messages using streamlit_chat
chat_container = st.container()
with chat_container:
    if st.session_state.messages:
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                message(msg["content"], is_user=True, key=f"{i}_user")
            else:
                message(msg["content"], is_user=False, key=f"{i}_assistant")
    else:
        # Welcome message
        st.markdown(
            f"""
            <div style="text-align: center; padding: 3rem 1rem; color: {DUKE_GRAY}; margin-top: 3rem;">
                <h3>Welcome to Duke Student Advisor!</h3>
                <p>How can I help you today?</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Add spacing for the fixed input field
st.markdown("<div style='height: 130px'></div>", unsafe_allow_html=True)

# User input at the bottom
input_container = st.container()
with input_container:
    st.markdown(
        """
        <div class="input-container">
        """,
        unsafe_allow_html=True
    )
    

    st.text_input("Type your message...", key="user_input", on_change=process_message, placeholder="Type your message...")
 

# Footer
st.markdown(
    f"""
    <div style="text-align: center; padding: 1rem; color: {DUKE_GRAY}; margin-top: 0rem;">
        <p>Duke University AI Student Advisor • Created for educational purposes</p>
    </div>
    """,
    unsafe_allow_html=True
)