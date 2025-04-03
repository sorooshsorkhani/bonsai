import pprint
from app.backend.graph.rag_graph import create_rag_graph


def nodes_output(graph, inputs):
    for output in graph.stream(inputs):
        for key, value in output.items():
            pprint.pprint(f"Output from node '{key}':")
            pprint.pprint("---")
            pprint.pprint(value, indent=2, width=80, depth=None)
        pprint.pprint("\n---\n")


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
            ("user", "What is an EBV? Make an example too."),
        ]
    }
    graph = create_rag_graph()

    #nodes_output(graph, inputs)
    node_tokens(graph, inputs)