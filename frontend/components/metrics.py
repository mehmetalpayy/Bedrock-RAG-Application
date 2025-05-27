import streamlit as st
from utils import AWSClient


def render_metrics():
    """Render metrics at the bottom of the page"""
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Yüklenen Dosya", len(st.session_state.uploaded_files))

    with col2:
        st.metric("Chat Sayısı", len([m for m in st.session_state.chat_history if m['role'] == 'user']))

    with col3:
        aws_client = AWSClient()
        connection_status = "✅ AWS Bağlantısı" if aws_client.check_aws_connection() else "❌ AWS Bağlantısı"
        if aws_client.check_aws_connection():
            st.success(connection_status)
        else:
            st.error(connection_status)