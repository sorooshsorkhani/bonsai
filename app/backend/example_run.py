import pprint
from app.backend.graph.rag_graph import create_rag_graph


inputs = {
    "messages": [
        ("user", "What is an EBV?"),
    ]
}

graph = create_rag_graph()

for output in graph.stream(inputs):
    for key, value in output.items():
        pprint.pprint(f"Output from node '{key}':")
        pprint.pprint("---")
        pprint.pprint(value, indent=2, width=80, depth=None)
    pprint.pprint("\n---\n")