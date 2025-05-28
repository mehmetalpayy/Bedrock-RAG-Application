import streamlit as st
from components import render_sidebar, render_chat, render_metrics
from utils import init_session_state
from config import PAGE_CONFIG

st.set_page_config(**PAGE_CONFIG)

st.title("🧠 Agentic RAG Chat Application")
st.subheader('RAG Using Knowledge Base from Amazon Bedrock', divider='rainbow')

init_session_state()

render_sidebar()

render_chat()

render_metrics()