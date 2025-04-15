from app.backend.agents import AgentState
from app.backend.tools.retriever_tool import doc_retriever




def additional_retrieve(state: AgentState):
    """
    Retrieves additional documents.

    Args:
        state (messages): The current messages state
        state (documents): The current documents state

    Returns:
        dict: The updated state with more documents
    """

    print("---ADDITIONAL RETRIEVE---")

    generated_queries = state['messages'][-1]
    docs = set()

    for q in generated_queries:
        retrieved_docs = doc_retriever(q)
        docs.update(retrieved_docs)
    
    docs = list(docs)

    return {'documents': docs}
