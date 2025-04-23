import streamlit as st
from app.backend.run_backend import stream_response  # Uses the preloaded graph
from app.frontend.feedback.feedback_manager import record_feedback  # our feedback helper

# Set Streamlit Page Configuration
st.set_page_config(page_title="BONsAI", page_icon="🌍")

st.title("🌍 BONsAI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 1️⃣ Re-display all previous messages (and their feedback buttons)
for idx, (role, content) in enumerate(st.session_state.messages):
    with st.chat_message(role):
        st.markdown(content)

    if role == "assistant":
        col1, col2 = st.columns([1, 1])
        if col1.button("👍", key=f"thumbs_up_{idx}"):
            record_feedback(idx, content, "up")
            st.success("👍 Thanks for your feedback!")
        if col2.button("👎", key=f"thumbs_down_{idx}"):
            record_feedback(idx, content, "down")
            st.error("👎 Got it, thanks!")

# 2️⃣ Get new user input
user_input = st.chat_input("Type your message...")

if user_input:
    # ➡️ Append and show the user's message
    st.session_state.messages.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # ➡️ Stream the assistant response
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""

        for chunk in stream_response(user_input):
            full_response += chunk
            response_container.markdown(full_response)

        # ➡️ Save the complete assistant message into session_state
        st.session_state.messages.append(("assistant", full_response))

        # ────────────────
        # ✨ IMMEDIATE FEEDBACK BUTTONS
        # Now that the message is fully rendered, show 👍/👎 right away:
        idx = len(st.session_state.messages) - 1  # index of this new assistant msg
        col1, col2 = st.columns([1, 1])
        if col1.button("👍", key=f"thumbs_up_{idx}"):
            record_feedback(idx, full_response, "up")
            st.success("👍 Thanks for your feedback!")
        if col2.button("👎", key=f"thumbs_down_{idx}"):
            record_feedback(idx, full_response, "down")
            st.error("👎 Got it, thanks!")
        # ────────────────
