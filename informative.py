from function import user_input, clear_chat_history
import streamlit as st

def informative_mode():
    st.sidebar.button('Effacer l\'historique du chat', on_click=clear_chat_history)
    
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.chat_history += f'User: {prompt}\n'

        # Pass None for difficulty in informative mode
        response = user_input(prompt, 1, [], st.session_state.chat_history, None)
        full_response = ''.join(response['output_text'])

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.session_state.chat_history += f'Assistant: {full_response}\n'

    # Display all messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])