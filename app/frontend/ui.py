import streamlit as st
from app.backend.run_backend import stream_response
from app.frontend.feedback.feedback_manager import record_feedback

# ─── Initialization ──────────────────────────────────────────────────────────

st.set_page_config(page_title="BONsAI", page_icon="🌍")
st.title("🌍 BONsAI")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "feedback_status" not in st.session_state:
    st.session_state.feedback_status = {}

if "last_seen" not in st.session_state:
    st.session_state.last_seen = 0


# ─── 1) Render history up to last_seen ────────────────────────────────────────

for idx, (role, content) in enumerate(st.session_state.messages):
    if idx >= st.session_state.last_seen:
        break

    with st.chat_message(role):
        st.markdown(content)

    if role == "assistant":
        prev_user = None
        if idx > 0 and st.session_state.messages[idx - 1][0] == "user":
            prev_user = st.session_state.messages[idx - 1][1]

        status = st.session_state.feedback_status.get(idx)

        # If never-rated or pending comment, we reuse the same unified UI
        if status is None or status == "comment_pending":
            col1, col2 = st.columns(2)

            if status is None:
                if col1.button("👍", key=f"up_{idx}"):
                    record_feedback(idx, content, "up", user_input=prev_user)
                    st.session_state.feedback_status[idx] = "up"
                    st.success("👍 Thanks for your feedback!")
                if col2.button("👎", key=f"down_{idx}"):
                    st.session_state.feedback_status[idx] = "comment_pending"

            # comment-pending:
            status = st.session_state.feedback_status.get(idx)
            if status == "comment_pending":
                comment = st.text_area("What went wrong? (optional)", key=f"comment_{idx}")
                sub_col, skip_col = st.columns(2)
                if sub_col.button("Submit", key=f"submit_{idx}"):
                    record_feedback(
                        idx, content, "down",
                        user_input=prev_user,
                        comment=comment.strip() or None
                    )
                    st.session_state.feedback_status[idx] = "down"
                    st.success("🙏 Thanks for your feedback!")
                if skip_col.button("Skip", key=f"skip_{idx}"):
                    record_feedback(
                        idx, content, "down",
                        user_input=prev_user,
                        comment=None
                    )
                    st.session_state.feedback_status[idx] = "down"
                    st.info("Skipped—thanks!")

        else:
            # Already “up” or “down” → show only the clicked button, disabled
            if status == "up":
                st.button("👍", key=f"up_done_{idx}", disabled=True)
            elif status == "down":
                st.button("👎", key=f"down_done_{idx}", disabled=True)


# ─── 2) Handle new input & immediate feedback ─────────────────────────────────

user_input = st.chat_input("Type your message...")

if user_input:
    # show & save user message
    st.session_state.messages.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # stream assistant response
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        for chunk in stream_response(user_input):
            full_response += chunk
            response_container.markdown(full_response)

    # append assistant message & init feedback
    assistant_idx = len(st.session_state.messages)
    st.session_state.messages.append(("assistant", full_response))
    st.session_state.feedback_status[assistant_idx] = None

    # immediate feedback UI
    prev_user = user_input
    status = st.session_state.feedback_status.get(assistant_idx)

    if status is None or status == "comment_pending":
        col1, col2 = st.columns(2)

        if status is None:
            if col1.button("👍", key=f"up_{assistant_idx}"):
                record_feedback(assistant_idx, full_response, "up", user_input=prev_user)
                st.session_state.feedback_status[assistant_idx] = "up"
                st.success("👍 Thanks for your feedback!")
            if col2.button("👎", key=f"down_{assistant_idx}"):
                st.session_state.feedback_status[assistant_idx] = "comment_pending"

        status = st.session_state.feedback_status.get(assistant_idx)
        if status == "comment_pending":
            comment = st.text_area("What went wrong? (optional)", key=f"comment_{assistant_idx}")
            sub_col, skip_col = st.columns(2)
            if sub_col.button("Submit", key=f"submit_{assistant_idx}"):
                record_feedback(
                    assistant_idx, full_response, "down",
                    user_input=prev_user,
                    comment=comment.strip() or None
                )
                st.session_state.feedback_status[assistant_idx] = "down"
                st.success("🙏 Thanks for your feedback!")
            if skip_col.button("Skip", key=f"skip_{assistant_idx}"):
                record_feedback(
                    assistant_idx, full_response, "down",
                    user_input=prev_user,
                    comment=None
                )
                st.session_state.feedback_status[assistant_idx] = "down"
                st.info("Skipped—thanks!")

    else:
        # show only the chosen button, disabled
        if status == "up":
            st.button("👍", key=f"up_done_{assistant_idx}", disabled=True)
        else:  # down
            st.button("👎", key=f"down_done_{assistant_idx}", disabled=True)

    # mark that we’ve fully rendered this turn
    st.session_state.last_seen = len(st.session_state.messages)
