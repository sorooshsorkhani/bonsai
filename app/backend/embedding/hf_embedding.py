from langchain_huggingface import HuggingFaceEmbeddings

def load_embedding(model_name="all-MiniLM-L6-v2"):
    """
    Loads the Hugging Face embeddings model.
    
    Args:
        model_name (str): Name of the Hugging Face model to load.
        
    Returns:
        HuggingFaceEmbeddings: The initialized embeddings model.
    """
    return HuggingFaceEmbeddings(model_name=model_name)
