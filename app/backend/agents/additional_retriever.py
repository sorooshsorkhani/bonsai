# app/backend/agents/additional_retrieve.py

from langchain_core.messages import BaseMessage
from app.backend.tools.retriever_tool import doc_retriever
from app.backend.agents.agent_state import AgentState

def additional_retrieve(state: AgentState) -> dict:
    """
    Retrieves additional documents based on the last-generated queries,
    and returns them so that add_documents will merge/dedupe them.
    """
    print("---ADDITIONAL RETRIEVE---")

    # Pull the generated_queries list off the last message
    last_msg = state["messages"][-1]
    queries = last_msg.content if isinstance(last_msg, BaseMessage) else last_msg

    # Normalize to a list of strings
    if isinstance(queries, str):
        queries = [queries]
    elif not isinstance(queries, list):
        queries = list(queries)

    all_new_docs = []
    for q in queries:
        # call the raw function, get (summary, docs)
        summary, docs = doc_retriever.func(q)
        all_new_docs.extend(docs)
    return {"documents": all_new_docs}
