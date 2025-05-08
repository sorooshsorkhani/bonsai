from app.backend.graph.rag_graph import create_rag_graph
from app.backend.errors.error_handler import handle_groq_error

# Initialize the graph only once
print("Initializing RAG Graph... This may take some time.")
rag_graph = create_rag_graph()
print("RAG Graph initialized successfully.")

def stream_response(user_input):
    """
    Streams the response from the LangGraph RAG model.

    Args:
        user_input (str): User's query.

    Yields:
        str: Response tokens from the model.
    """
    inputs = {"messages": [("user", user_input)]}

    try:
        for msg, metadata in rag_graph.stream(inputs, stream_mode="messages"):
            if msg.content and metadata["langgraph_node"] in ["rag", "greetings"]:
                yield msg.content
                
    except Exception as e:
        yield handle_groq_error(e)