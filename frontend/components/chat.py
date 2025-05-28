import streamlit as st
from utils import add_message
import requests
import os


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def get_rag_answer(question: str):
    try:
        response = requests.post(
            f"{BACKEND_URL}/retrieve_chunks",
            json={
                "query": question
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Backend error: {e}")
        return None


def render_chat():
    for message in st.session_state.chat_history:
        with st.chat_message(message['role']):
            st.markdown(message['text'])
            if message['role'] == 'assistant':
                if message['context']:
                    st.markdown(f"<span style='color:#FFDA33'>**Context:** </span>{message['context']}", unsafe_allow_html=True)
                if message['source']:
                    st.markdown(f"<span style='color:#FFDA33'>**Source:** </span>{message['source']}", unsafe_allow_html=True)

    question = st.chat_input('Type your question here...')
    if question:
        with st.chat_message('user'):
            st.markdown(question)
        add_message('user', question)

        with st.chat_message('assistant'):
            with st.spinner("Thinking..."):
                response = get_rag_answer(question)
                if response:
                    answer = response['answer']
                    st.markdown(answer)
                    add_message('assistant', answer, "", "")
        st.rerun()