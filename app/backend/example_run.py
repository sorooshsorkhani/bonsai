import pprint
from app.backend.graph.rag_graph import create_rag_graph

inputs = {
    "messages": [
        ("user", "I need a tool in BON in a Box that can help me with the study of species population."
        "Also, whom can I contact to ask more about the tool?"),
    ]
}

graph = create_rag_graph()

for output in graph.stream(inputs):
    for key, value in output.items():
        pprint.pprint(f"Output from node '{key}':")
        pprint.pprint("---")
        pprint.pprint(value, indent=2, width=80, depth=None)
    pprint.pprint("\n---\n")