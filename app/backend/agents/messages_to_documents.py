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

    last_message = state['messages'][-1]
    docs = last_message.content
    
    return {"documents": docs}