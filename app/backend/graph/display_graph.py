from app.backend.graph.rag_graph import create_rag_graph
import os

rag_graph = create_rag_graph()

try:
    # Save the generated image to a file
    image_path = "graph_image.png"
    with open(image_path, "wb") as f:
        f.write(rag_graph.get_graph(xray=True).draw_mermaid_png())
    
    print(f"Image saved to {os.path.abspath(image_path)}")

except Exception as e:
    print(f"An error occurred: {e}")
