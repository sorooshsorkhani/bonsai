import streamlit as st
from app.backend.run_backend import stream_response
from app.frontend.feedback.feedback_manager import record_feedback

# Set Streamlit Page Configuration
st.set_page_config(page_title="BONsAI", page_icon="🌍")
st.title("🌍 BONsAI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 1️⃣ Re-display all previous messages + feedback buttons
for idx, (role, content) in enumerate(st.session_state.messages):
    with st.chat_message(role):
        st.markdown(content)

    if role == "assistant":
        # The user's input is the message just before this one.
        prev_user = None
        if idx > 0 and st.session_state.messages[idx - 1][0] == "user":
            prev_user = st.session_state.messages[idx - 1][1]

        col1, col2 = st.columns([1, 1])
        if col1.button("👍", key=f"thumbs_up_{idx}"):
            record_feedback(idx, content, "up", user_input=prev_user)
            st.success("👍 Thanks for your feedback!")
        if col2.button("👎", key=f"thumbs_down_{idx}"):
            record_feedback(idx, content, "down", user_input=prev_user)
            st.error("👎 Got it, thanks!")

# 2️⃣ User input
user_input = st.chat_input("Type your message...")

if user_input:
    # ➡️ Append & show the user's message
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

        # ➡️ Save assistant response
        st.session_state.messages.append(("assistant", full_response))

        # ────────────────
        # ✨ Show feedback buttons immediately
        idx = len(st.session_state.messages) - 1
        # The triggering user input is the one we just added above.
        prev_user = user_input

        col1, col2 = st.columns([1, 1])
        if col1.button("👍", key=f"thumbs_up_{idx}"):
            record_feedback(idx, full_response, "up", user_input=prev_user)
            st.success("👍 Thanks for your feedback!")
        if col2.button("👎", key=f"thumbs_down_{idx}"):
            record_feedback(idx, full_response, "down", user_input=prev_user)
            st.error("👎 Got it, thanks!")
        # ────────────────
