from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import streamlit as st
from conversation import get_conversational_chain

# Function to read lists from CSV
def read_lists_from_csv(file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        L1 = df['Easy'].dropna().tolist()
        L2 = df['Medium'].dropna().tolist()
        L3 = df['Hard'].dropna().tolist()
        M1 = df['M1'].dropna().tolist()
        M2 = df['M2'].dropna().tolist()
        M3 = df['M3'].dropna().tolist()
    else:
        L1 = ['Ket', 'Superposition', 'Interpretation statistique']
        L2 = ['Etat lié', 'Etat de diffusion', 'Equation de Schrodinger']
        L3 = ['Oscillateur harmonique', 'Particule libre', 'Fonction onde']
        M1, M2, M3 = [], [], []
    return L1, L2, L3, M1, M2, M3

# Function to write lists to CSV
def write_lists_to_csv(file_path, L1, L2, L3, M1, M2, M3):
    df = pd.DataFrame({
        'Easy': pd.Series(L1),
        'Medium': pd.Series(L2),
        'Hard': pd.Series(L3),
        'M1': pd.Series(M1),
        'M2': pd.Series(M2),
        'M3': pd.Series(M3)
    })
    df.to_csv(file_path, index=False)

# Read all PDF files and return text
def get_pdf_text_from_directory(directory):
    text = ""
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            pdf_reader = PdfReader(pdf_path)
            for page in pdf_reader.pages:
                text += page.extract_text()
    return text

# Split text into chunks
def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000, chunk_overlap=1000)
    chunks = splitter.split_text(text)
    return chunks  # list of strings

# Get embeddings for each chunk
def get_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001")  # type: ignore
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    
def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "Bienvenue 😊"}]
    st.session_state.chat_history = ''
    st.session_state.difficulty = None
    st.session_state.active_list = None
    st.session_state.active_m_list = None
    st.session_state.current_notion = None  #

def user_input(user_question, a, L, chat_history, difficulty):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001")  # type: ignore

    new_db = FAISS.load_local(
        "faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain(a, L, chat_history, difficulty)

    response = chain(
        {"input_documents": docs, "question": user_question, "chat_history": chat_history}, return_only_outputs=True)

    print(response)
    return response