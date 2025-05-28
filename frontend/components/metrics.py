import streamlit as st
from utils import AWSClient


def render_metrics():
    """Render metrics at the bottom of the page"""
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Uploaded Files", len(st.session_state.uploaded_files))

    with col2:
        st.metric("Chat Count", len([m for m in st.session_state.chat_history if m['role'] == 'user']))

    with col3:
        aws_client = AWSClient()
        connection_status = "✅ AWS Connected" if aws_client.check_aws_connection() else "❌ AWS Not Connected"
        if aws_client.check_aws_connection():
            st.success(connection_status)
        else:
            st.error(connection_status)