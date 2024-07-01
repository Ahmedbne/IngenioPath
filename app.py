import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from informative import informative_mode
from game import game_mode
from quiz import quiz_mode
from function import get_pdf_text_from_directory, get_text_chunks, get_vector_store

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
PDF_DIRECTORY = "./PDF"

def main():
    # Custom CSS with enhanced styling
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    body {
        font-family: 'Poppins', sans-serif;
        background-color: #f0f2f6;
    }
    
    .main-title {
        font-family: 'Poppins', sans-serif;
        font-size: 4em;
        font-weight: 700;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        display: inline-block;
    }
    
    .subtitle {
        font-family: 'Poppins', sans-serif;
        font-size: 1.5em;
        color: #45B7D1;
        margin-bottom: 30px;
    }
    
    .sidebar-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.8em;
        font-weight: 600;
        color: #FF6B6B;
        margin-bottom: 20px;
    }
    
    .stButton>button {
        background-color: #4ECDC4;
        color: white;
        font-weight: bold;
        border-radius: 25px;
        padding: 12px 24px;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        background-color: #45B7D1;
        transform: translateY(-3px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }
    
    .stSelectbox {
        border-radius: 15px;
        border: 2px solid #4ECDC4;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .logo-image {
        border-radius: 15px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        width: 150px;
        height: auto;
        object-fit: cover;
        margin-right: 20px;
    }
    
    .logo-image:hover {
        transform: scale(1.1) rotate(5deg);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .stTextInput>div>div>input {
        border-radius: 20px;
        border: 2px solid #4ECDC4;
        padding: 10px 15px;
    }

    .stTextInput>div>div>input:focus {
        outline: none;
        border: 2px solid #45B7D1;
    }
    
    .chat-message {
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        display: flex;
        align-items: flex-start;
    }
    
    .chat-message.user {
        background-color: #E0F7FA;
    }
    
    .chat-message.assistant {
        background-color: #FFF9C4;
    }
    
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 10px;
    }
    
    .chat-message .message-content {
        flex-grow: 1;
    }
    
    .mode-title {
        font-family: 'Poppins', sans-serif;
        font-size: 2.5em;
        font-weight: 700;
        color: #45B7D1;
        margin-bottom: 10px;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    .mode-description {
        font-family: 'Poppins', sans-serif;
        font-size: 1.2em;
        color: #6C757D;
        margin-bottom: 30px;
    }
    
    .mode-button {
    display: block;
    width: 100%;
    padding: 15px;
    margin: 10px 0;
    font-size: 1.2em;
    font-weight: 600;
    color: white;
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
    border: none;
    border-radius: 15px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
}

.mode-button:hover {
    background: linear-gradient(45deg, #4ECDC4, #FF6B6B);
    transform: translateY(-3px);
    box-shadow: 0 6px 8px rgba(0,0,0,0.15);
}

.sidebar-title {
    font-family: 'Poppins', sans-serif;
    font-size: 1.8em;
    font-weight: 600;
    color: #FF6B6B;
    margin-bottom: 20px;
}

    </style>
    """, unsafe_allow_html=True)

    # Ensure session state variables are initialized
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Bienvenue à IngenioPath ! Comment puis-je vous aider aujourd'hui ? 😊"}]
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = ''
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = None
    if "active_list" not in st.session_state:
        st.session_state.active_list = None
    if "active_m_list" not in st.session_state:
        st.session_state.active_m_list = None

    # Sidebar for mode selection
    st.sidebar.markdown('<p class="sidebar-title">Navigation</p>', unsafe_allow_html=True)
    mode = st.sidebar.selectbox("Choisissez le mode:", options=["Informatif", "Devinette", "Quiz"])

    # Display title with image
    st.markdown(f'<div class="logo-container"><img src="https://i.imghippo.com/files/mAdAC1719466880.jpg" class="logo-image"><p class="main-title">IngenioPath 🤖</p></div>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Votre assistant d\'apprentissage intelligent</p>', unsafe_allow_html=True)

    with st.spinner("Chargement en cours..."):
        raw_text = get_pdf_text_from_directory(PDF_DIRECTORY)
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
    st.success("Prêt à commencer !")

    if mode == "Informatif":
        st.markdown('<h2 class="mode-title">Informative Mode</h2>', unsafe_allow_html=True)
        st.markdown('<p class="mode-description">Bienvenue dans le mode informatif ! Posez vos questions.</p>', unsafe_allow_html=True)
        informative_mode()
    elif mode == "Devinette":
        st.markdown('<h2 class="mode-title">Devinette</h2>', unsafe_allow_html=True)
        st.markdown('<p class="mode-description">Bienvenue dans le mode Devinette ! Prêt à jouer ?</p>', unsafe_allow_html=True)
        game_mode()
    else:
        st.markdown('<h2 class="mode-title">Quiz Mode</h2>', unsafe_allow_html=True)
        st.markdown('<p class="mode-description">Bienvenue dans le mode quiz ! Testez vos connaissances.</p>', unsafe_allow_html=True)
        quiz_mode()

if __name__ == "__main__":
    main()
