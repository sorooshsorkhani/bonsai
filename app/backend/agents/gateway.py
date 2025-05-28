from app.backend.llm.groq import GroqLLM
from app.backend.agents.agent_state import AgentState
from app.backend.tools.retriever_tool import doc_retriever


def gateway(state: AgentState):
    """
    Invokes the gateway model to generate a response based on the current state. Given
    the query, it will decide to retrieve using the retriever tool, or simply end.

    Args:
        state (messages): The current state
        state (documents): The current documents state
        
    Returns:
        dict: The updated state with the gateway response appended to messages
    """
    print("---CALL GATEWAY---")
    messages = state["messages"]
    model = GroqLLM.load_llm()
    gateway_model = model.bind_tools(tools=[doc_retriever], tool_choice="any")
    response = gateway_model.invoke(messages)
    print(response)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

    ## pull the real list off .artifact
    #docs = getattr(response, "artifact", None)
    #if docs is None:
    #    # fallback if artifact wasn’t set
    #    return {"documents": []}
    #return {"documents": docs}

