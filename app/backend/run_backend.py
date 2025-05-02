from app.backend.graph.rag_graph import create_rag_graph
from groq import RateLimitError

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
            if msg.content and metadata["langgraph_node"] == "rag":
                yield msg.content
            if msg.content and metadata["langgraph_node"] == "greetings":
                yield msg.content

    except RateLimitError:
        # Yield a special marker that UI can detect
        yield "[ERROR:RATE_LIMIT]"