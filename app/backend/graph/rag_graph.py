from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from app.backend.tools.retriever_tool import doc_retriever
from app.backend.agents import AgentState, gateway, grade_relevance, rag, rewrite, greet
from langgraph.graph.graph import CompiledGraph

def create_rag_graph() -> CompiledGraph:

    # Define a new graph
    workflow = StateGraph(AgentState)

    # Define the nodes we will cycle between
    workflow.add_node("gateway", gateway)  # agent
    retrieve = ToolNode([doc_retriever])
    workflow.add_node("retrieve", retrieve)  # retrieval
    workflow.add_node("greetings", greet)
    #workflow.add_node("rewrite", rewrite)  # Re-writing the question
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

    # Edges taken after the `action` node is called.
    workflow.add_conditional_edges(
        "retrieve",
        # Assess agent decision
        grade_relevance,
    )

    # add sufficiency condition

    workflow.add_edge("rag", END)
    #workflow.add_edge("rewrite", "gateway")

    # Compile
    rag_graph = workflow.compile()
    return rag_graph

