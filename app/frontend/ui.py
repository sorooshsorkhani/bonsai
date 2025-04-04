import streamlit as st
from app.backend.run_backend import stream_response  # Uses the preloaded graph

# Set Streamlit Page Configuration
st.set_page_config(page_title="BONsAI", page_icon="🌍")

st.title("🌍 BONsAI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role, content = message
    with st.chat_message(role):
        st.markdown(content)

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Store user input in chat history
    st.session_state.messages.append(("user", user_input))

    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate and stream response
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""

        for chunk in stream_response(user_input):
            full_response += chunk
            response_container.markdown(full_response)

        # Store assistant response in chat history
        st.session_state.messages.append(("assistant", full_response))
