from typing import Annotated, Sequence
from typing_extensions import TypedDict, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_core.documents import Document

def add_documents(existing: List[Document] | None, new:List[Document] | None) -> List[Document]:
    # If nothing yet, start with an empty list
    if existing is None:
        existing = []

    # If no new docs, just return what we have
    if not new:
        return existing

    # For each incoming doc, only append if it's not already in the list
    for doc in new:
        if doc not in existing:
            existing.append(doc)

    return existing


class AgentState(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    messages: Annotated[Sequence[BaseMessage], add_messages]
    documents: Annotated[Sequence[Document], add_documents]
