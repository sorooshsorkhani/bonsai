from app.backend.agents import AgentState
from app.backend.tools.retriever_tool import doc_retriever




def additional_retrieve(state: AgentState) -> dict:
    """
    Retrieves additional documents.

    Args:
        state (messages): The current messages state
        state (documents): The current documents state

    Returns:
        dict: The updated state with more documents
    """

    print("---ADDITIONAL RETRIEVE---")

    # The last message is our list of new query strings
    queries = state["messages"][-1]
    if not isinstance(queries, list):
        queries = [queries]

    all_new_docs = []
    for q in queries:
        # doc_retriever returns (summary, List[Document])
        _, new_docs = doc_retriever(q)
        all_new_docs.extend(new_docs)

    # Return ONLY the newly fetched docs; add_documents will append + dedupe
    return {"documents": all_new_docs}
