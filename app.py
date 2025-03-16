import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from googletrans import Translator
import os

# Load API key from a file
def load_api_key(filepath):
    try:
        with open(filepath, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        raise Exception(f"❌ API key file '{filepath}' not found!")

GOOGLE_API_KEY = load_api_key("gemini1.txt")

# Streamlit Page Configuration
st.set_page_config(page_title="AI Data Science Tutor Chatbot", layout="centered")

# Page Title
st.markdown("<h1 style='text-align: center;'>🤖 AI Data Science Tutor Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Chat with an AI-powered Data Science expert</h4>", unsafe_allow_html=True)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are an AI-powered Data Science tutor. Provide clear, engaging explanations, step-by-step guidance, and examples on any Data Science topic.")
    ]

# Display Chat Messages
for msg in st.session_state.messages[1:]:  # Skip system message
    with st.chat_message("user" if isinstance(msg, HumanMessage) else "assistant"):
        st.markdown(msg.content)

# Function to Get AI-generated Response
def get_chat_response(conversation_history):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=GOOGLE_API_KEY)
    try:
        response = llm.invoke(conversation_history)
        return response.content if response else "⚠ No response from AI."
    except Exception as e:
        return f"❌ Error fetching response: {str(e)}"

# Chat Input
user_input = st.chat_input("Ask a Data Science question...")
if user_input:
    # Add user input to chat history
    st.session_state.messages.append(HumanMessage(content=user_input))
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate AI Response based on conversation history
    with st.spinner("🤖 Thinking..."):
        ai_response = get_chat_response(st.session_state.messages)
    
    st.session_state.messages.append(SystemMessage(content=ai_response))
    with st.chat_message("assistant"):
        st.markdown(ai_response)

# Footer
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            width: 100%;
            text-align: center;
            padding: 10px;
            background-color: #f1f1f1;
            color: #333333;
            font-weight: bold;
            border-top: 2px solid #cccccc;
            z-index: 9999;
        }
    </style>
    <div class="footer">
        Created by Paul Andrew D 🚀
    </div>
    """,
    unsafe_allow_html=True
)
