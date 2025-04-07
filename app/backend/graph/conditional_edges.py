from app.backend.agents.agent_state import AgentState

def should_retrieve(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    # If there is no function call, then we finish
    if not last_message.tool_calls:
        return "greetings"
    # Otherwise if there is, we continue
    else:
        return "should_retrieve"