from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from app.backend.tools.retriever_tool import doc_retriever
from langgraph.graph.graph import CompiledGraph
from app.backend.agents import (
    AgentState,
    gateway,
    grade_relevance,
    grade_sufficiency,
    rag,
    greet,
    generate_queries,
    additional_retrieve,
    msg_to_docs,
)

def create_rag_graph() -> CompiledGraph:
    # Initialize the graph with our AgentState schema
    workflow = StateGraph(AgentState)

    # Define core nodes
    workflow.add_node("gateway", gateway)
    retrieve = ToolNode([doc_retriever])
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("msg_to_docs", msg_to_docs)
    workflow.add_node("greetings", greet)
    workflow.add_node("generate_queries", generate_queries)
    workflow.add_node("additional_retrieve", additional_retrieve)
    workflow.add_node("rag", rag)
    # Placeholder node to branch on sufficiency
    workflow.add_node("grade_sufficiency", lambda state: {})

    # Start → gateway
    workflow.add_edge(START, "gateway")

    # Gateway decision: call tools or end
    workflow.add_conditional_edges(
        "gateway",
        tools_condition,
        {
            "tools": "retrieve",
            END: "greetings",
        },
    )
    workflow.add_edge("greetings", END)

    # Retrieval → normalize docs → relevance check
    workflow.add_edge("retrieve", "msg_to_docs")

    # Relevance branching: relevant → sufficiency, irrelevant → end
    workflow.add_conditional_edges(
        "msg_to_docs",
        grade_relevance,
        {
            "grade_sufficiency": "grade_sufficiency",
            "greetings": "greetings",
        },
    )

    # Sufficiency branching: sufficient → rag, insufficient → new queries
    workflow.add_conditional_edges(
        "grade_sufficiency",
        grade_sufficiency,
        {
            "rag": "rag",
            "generate_queries": "generate_queries",
        },
    )

    # Generate queries → additional retrieve → final RAG response
    workflow.add_edge("generate_queries", "additional_retrieve")
    workflow.add_edge("additional_retrieve", "rag")
    workflow.add_edge("rag", END)

    return workflow.compile()
