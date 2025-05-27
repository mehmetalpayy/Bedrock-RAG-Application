import streamlit as st
from utils import AWSClient, add_uploaded_file, clear_chat_history
from config import UPLOAD_CONFIG


def render_sidebar():
    """Render the sidebar with file upload functionality"""
    with st.sidebar:
        st.header("📁 Dosya Yükleme")
        
        uploaded_files = st.file_uploader(
            "Dosyalarınızı seçin",
            accept_multiple_files=UPLOAD_CONFIG["multiple_files"],
            type=UPLOAD_CONFIG["allowed_types"]
        )
        
        aws_client = AWSClient()
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                if uploaded_file.name not in [f['name'] for f in st.session_state.uploaded_files]:
                    with st.spinner(f"{uploaded_file.name} yükleniyor..."):
                        s3_path = aws_client.upload_to_s3(uploaded_file, uploaded_file.name)
                        if s3_path:
                            add_uploaded_file(uploaded_file.name, s3_path)
                            st.success(f"✅ {uploaded_file.name} yüklendi!")
        
        if st.session_state.uploaded_files:
            st.write("**Yüklenen Dosyalar:**")
            for file_info in st.session_state.uploaded_files:
                st.write(f"• {file_info['name']}")
        
        if st.button("🗑️ Chat Geçmişini Temizle", use_container_width=True):
            clear_chat_history()
            st.rerun()