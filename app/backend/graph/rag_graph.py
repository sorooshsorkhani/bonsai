from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from app.backend.tools.retriever_tool import doc_retriever
from langgraph.graph.graph import CompiledGraph
from app.backend.agents import (AgentState, 
    gateway, 
    grade_relevance, 
    grade_sufficiency, 
    rag, 
    greet, 
    generate_queries, 
    additional_retrieve, 
    msg_to_docs
    )

def create_rag_graph() -> CompiledGraph:

    # Define a new graph
    workflow = StateGraph(AgentState)

    # Define the nodes we will cycle between
    workflow.add_node("gateway", gateway)  # agent
    retrieve = ToolNode([doc_retriever])
    workflow.add_node("retrieve", retrieve)  # retrieval
    workflow.add_node("msg_to_docs", msg_to_docs)
    workflow.add_node("grade_relevance", grade_relevance)
    workflow.add_node("grade_sufficiency", grade_sufficiency)
    workflow.add_node("greetings", greet)
    workflow.add_node("generate_queries", generate_queries)
    workflow.add_node("additional_retrieve", additional_retrieve)
    workflow.add_node("rag", rag)  # Generating a response after we know the documents are relevant
    
    # Call gateway node to decide to retrieve or not
    workflow.add_edge(START, "gateway")

    # Decide whether to retrieve
    workflow.add_conditional_edges(
        "gateway",
        # Assess agent decision
        tools_condition,
        {
            # Translate the condition outputs to nodes in our graph
            "tools": "retrieve",
            END: "greetings",
        },
    )
    workflow.add_edge("greetings", END)
    workflow.add_edge("retrieve", "msg_to_docs")
    workflow.add_edge("msg_to_docs", "grade_relevance")

    # Edges taken after the `action` node is called.
    workflow.add_conditional_edges(
        "grade_relevance", # this is a node
        # Assess agent decision
        grade_relevance, # this is a routing function
        {
        "grade_sufficiency": "grade_sufficiency",
        "greetings": "greetings",
        },
    )

    # add sufficiency condition
    # Edges taken after the `action` node is called.
    workflow.add_conditional_edges(
        "grade_sufficiency", # this is a node
        # Assess agent decision
        grade_sufficiency, # this is a routing function
        {
        "rag": "rag",
        "generate_queries": "generate_queries",
        },
    )

    workflow.add_edge("generate_queries", "additional_retrieve")
    workflow.add_edge("additional_retrieve", "rag")
    workflow.add_edge("rag", END)

    # Compile
    rag_graph = workflow.compile()
    return rag_graph

