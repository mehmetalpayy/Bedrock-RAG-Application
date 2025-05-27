import streamlit as st
from utils import add_message
import requests


BACKEND_URL = "http://localhost:8000/chat"


def get_backend_answer(question: str):
    try:
        response = requests.post(
            BACKEND_URL,
            json={"user_input": question},
            timeout=30
        )
        response.raise_for_status()
        return response.json()["answer"]
    except Exception as e:
        st.error(f"Backend error: {e}")
        return None


def render_chat():
    """Render the chat interface"""
    for message in st.session_state.chat_history:
        with st.chat_message(message['role']):
            st.markdown(message['text'])
            
            if message['role'] == 'assistant':
                if message['context']:
                    st.markdown(f"<span style='color:#FFDA33'>**Context:** </span>{message['context']}", unsafe_allow_html=True)
                if message['source']:
                    st.markdown(f"<span style='color:#FFDA33'>**Kaynak:** </span>{message['source']}", unsafe_allow_html=True)

    question = st.chat_input('Sorunuzu buraya yazın...')
    
    if question:
        with st.chat_message('user'):
            st.markdown(question)
        add_message('user', question)
        
        with st.chat_message('assistant'):
            with st.spinner("Düşünüyorum..."):
                response = get_backend_answer(question)
            
            if response:
                answer = response['output']['text']
                st.markdown(answer)
                
                context = ""
                source = ""
                
                try:
                    if (response.get('citations') and 
                        len(response['citations']) > 0 and 
                        len(response['citations'][0].get('retrievedReferences', [])) > 0):
                        
                        context = response['citations'][0]['retrievedReferences'][0]['content']['text']
                        source = response['citations'][0]['retrievedReferences'][0]['location']['s3Location']['uri']
                        
                        if len(context) > 500:
                            context = context[:500] + "..."
                        
                        st.markdown(f"<span style='color:#FFDA33'>**Context:** </span>{context}", unsafe_allow_html=True)
                        st.markdown(f"<span style='color:#FFDA33'>**Kaynak:** </span>{source}", unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"<span style='color:orange'>**Kaynak bilgisi alınamadı:** {e}</span>", unsafe_allow_html=True)
                
                add_message('assistant', answer, context, source)