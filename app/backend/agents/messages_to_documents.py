from app.backend.agents.agent_state import AgentState


def msg_to_docs(state: AgentState):
    """
    Converts the documents wrapped in state messages to state documents

    Args:
        state (messages): The current state
        state (documents): The current documents state
        
    Returns:
        dict: The updated state with the documents
    """

    last = state["messages"][-1]
    state['messages'] = state['messages'][:-1]
    # pull the real list off .artifact
    docs = getattr(last, "artifact", None)
    if docs is None:
        # fallback if artifact wasn’t set
        return {"documents": []}
    return {"documents": docs}