import streamlit as st


def init_session_state():
    """Initialize session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []


def add_message(role: str, text: str, context: str = "", source: str = ""):
    """Add a message to chat history"""
    message = {
        "role": role,
        "text": text,
        "context": context,
        "source": source
    }
    st.session_state.chat_history.append(message)


def add_uploaded_file(name: str, s3_path: str):
    """Add an uploaded file to the session state"""
    st.session_state.uploaded_files.append({
        'name': name,
        's3_path': s3_path
    })


def clear_chat_history():
    """Clear chat history"""
    st.session_state.chat_history = []