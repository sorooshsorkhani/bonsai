from typing import Annotated, Sequence
from typing_extensions import TypedDict, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_core.documents import Document


class AgentState(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    #user_queries: Annotated[Sequence[BaseMessage], add_messages]
    user_queries: List[str]
    summary: str
    documents: List[Document]
    gen_queries: List[str]
