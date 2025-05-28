import pprint
from langchain_core.messages import HumanMessage
from langchain_core.documents import Document
from app.backend.graph.rag_graph import create_rag_graph
from app.backend.agents import generate_queries


def nodes_output(graph, inputs, config):
    for output in graph.stream(inputs, config=config):
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
    
    inputs1 = {
        "messages": [
            HumanMessage(content="What is an EBV?"),
        ],
        "documents": []
    
    }
    inputs2 = {
        "messages": [
            HumanMessage(content="Can you make an example?"),
        ],
        "documents": []
    
    }
    # Specify an ID for the thread
    config = {"configurable": {"thread_id": "2"}}
    
    graph = create_rag_graph()

    nodes_output(graph, inputs1, config=config)
    nodes_output(graph, inputs2, config=config)
    #node_tokens(graph, inputs)
    #run_node(inputs)
