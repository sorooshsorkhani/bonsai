from typing import Annotated, Sequence
from typing_extensions import TypedDict, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_core.documents import Document

def add_documents(existing: List[Document], new: List[Document]):
    existing_set = set(existing)  # relies on Document.__hash__ and __eq__

    for doc in new:
        if doc not in existing_set:
            existing.append(doc)
            existing_set.add(doc)


class AgentState(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    messages: Annotated[Sequence[BaseMessage], add_messages]
    documents: Annotated[Sequence[Document], add_documents]
