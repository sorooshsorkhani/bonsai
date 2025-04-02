from app.backend.llm.groq import GroqLLM
from app.backend.tools.retriever_tool import doc_retriever


def gateway(state):
    """
    Invokes the gateway model to generate a response based on the current state. Given
    the question, it will decide to retrieve using the retriever tool, or simply end.

    Args:
        state (messages): The current state
        
    Returns:
        dict: The updated state with the gateway response appended to messages
    """
    print("---CALL GATEWAY---")
    messages = state["messages"]
    model = GroqLLM.load_llm()
    gateway_model = model.bind_tools([doc_retriever])
    response = gateway_model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

