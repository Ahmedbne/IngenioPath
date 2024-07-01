import random
import streamlit as st
from function import read_lists_from_csv, write_lists_to_csv, user_input, clear_chat_history
from pdf_config import CSV_FILE

def game_mode():
    L1, L2, L3, M1, M2, M3 = read_lists_from_csv(CSV_FILE)

    
    if 'difficulty' not in st.session_state or st.session_state.difficulty is None:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('Facile'):
                st.session_state.difficulty = 'Facile'
                st.session_state.active_list = L1
                st.session_state.active_m_list = M1
        with col2:
            if st.button('Moyen'):
                st.session_state.difficulty = 'Moyen'
                st.session_state.active_list = L2
                st.session_state.active_m_list = M2
        with col3:
            if st.button('Difficile'):
                st.session_state.difficulty = 'Difficile'
                st.session_state.active_list = L3
                st.session_state.active_m_list = M3
    
    st.sidebar.button('Effacer l\'historique du chat', on_click=clear_chat_history)
    
    if st.session_state.difficulty is not None:
        if 'current_notion' not in st.session_state or st.session_state.current_notion is None:
            if st.session_state.active_list:
                st.session_state.current_notion = random.choice(st.session_state.active_list)
                print(f"Notion choisie : {st.session_state.current_notion}")  # Affichage dans le terminal
            else:
                print("Aucune notion disponible.")
                return

        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.chat_history += f'User: {prompt}\n'

            response = user_input(prompt, 0, st.session_state.active_list, st.session_state.chat_history, st.session_state.difficulty)
            full_response = ''.join(response['output_text'])

            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.chat_history += f'Assistant: {full_response}\n'

            if "C'est exact !" in full_response or "Veux-tu rejouer ?" in full_response:
                st.session_state.active_m_list.append(st.session_state.current_notion)
                st.session_state.active_list.remove(st.session_state.current_notion)
                if st.session_state.active_list:
                    st.session_state.current_notion = random.choice(st.session_state.active_list)
                    print(f"Nouvelle notion choisie : {st.session_state.current_notion}")  # Affichage dans le terminal
                else:
                    st.session_state.active_list = st.session_state.active_m_list
                    st.session_state.active_m_list = []
                    if st.session_state.active_list:
                        st.session_state.current_notion = random.choice(st.session_state.active_list)
                        print(f"Nouvelle notion choisie (reset) : {st.session_state.current_notion}")  # Affichage dans le terminal
                    else:
                        print("Toutes les notions ont été utilisées.")
                        st.session_state.current_notion = None

        # Display all messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Update the CSV file
        if st.session_state.difficulty == 'Facile':
            write_lists_to_csv(CSV_FILE, st.session_state.active_list, L2, L3, st.session_state.active_m_list, M2, M3)
        elif st.session_state.difficulty == 'Moyen':
            write_lists_to_csv(CSV_FILE, L1, st.session_state.active_list, L3, M1, st.session_state.active_m_list, M3)
        elif st.session_state.difficulty == 'Difficile':
            write_lists_to_csv(CSV_FILE, L1, L2, st.session_state.active_list, M1, M2, st.session_state.active_m_list)