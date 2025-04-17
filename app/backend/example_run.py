import pprint
from langchain_core.messages import HumanMessage
from langchain_core.documents import Document
from app.backend.graph.rag_graph import create_rag_graph
from app.backend.agents import generate_queries


def nodes_output(graph, inputs):
    for output in graph.stream(inputs):
        for key, value in output.items():
            pprint.pprint(f"Output from node '{key}':")
            pprint.pprint("---")
            pprint.pprint(value, indent=2, width=80, depth=None)
        pprint.pprint("\n---\n")

def run_node(inputs):
    response = generate_queries(inputs)
    print(response)
    return response

def node_tokens(graph, inputs):
    for msg, metadata in graph.stream(
        inputs,
        stream_mode="messages",
    ):
        if msg.content and metadata["langgraph_node"] == "rag":
            print(msg.content, end="", flush=True)


if __name__ == "__main__":
    
    inputs = {
        "messages": [
            HumanMessage(content="What is an EBV? Consider the documents not sufficient and generate more queries for additional retrieval"),
        ],
        "documents": []
    }
    graph = create_rag_graph()

    nodes_output(graph, inputs)
    #node_tokens(graph, inputs)
    #run_node(inputs)