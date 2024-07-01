import streamlit as st
from function import user_input, clear_chat_history

def quiz_mode():
    st.sidebar.button('Effacer l\'historique du chat', on_click=clear_chat_history)

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.chat_history += f'User: {prompt}\n'

        # Pass None for difficulty in quiz mode
        response = user_input(prompt, 2, [], st.session_state.chat_history, None)
        full_response = ''.join(response['output_text'])

        # Process the response to add line breaks for quiz choices
        processed_response = process_quiz_response(full_response)

        st.session_state.messages.append({"role": "assistant", "content": processed_response})
        st.session_state.chat_history += f'Assistant: {processed_response}\n'

    # Display all messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def process_quiz_response(response):
    lines = response.split('\n')
    processed_lines = []
    for line in lines:
        if line.strip().startswith(('A.', 'B.', 'C.', 'D.')):
            processed_lines.append('\n' + line)
        else:
            processed_lines.append(line)
    return '\n'.join(processed_lines)

