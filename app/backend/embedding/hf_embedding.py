from langchain_huggingface import HuggingFaceEmbeddings

import torch
torch.cuda.empty_cache()

AVAILABLE_MODELS = [
    "all-MiniLM-L6-v2",
    "static-similarity-mrl-multilingual-v1"
]

def load_embedding(model_name=AVAILABLE_MODELS[1]):
    """
    Loads a Hugging Face embeddings model.

    Args:
        model_name (str): Name of the Hugging Face model to load.
                          Must be one of the supported models.

    Returns:
        HuggingFaceEmbeddings: The initialized embeddings model.

    Available Models:
        - all-MiniLM-L6-v2
        - static-similarity-mrl-multilingual-v1
    """
    if model_name not in AVAILABLE_MODELS:
        raise ValueError(f"Unsupported model '{model_name}'. Choose from: {AVAILABLE_MODELS}")
    return HuggingFaceEmbeddings(model_name=model_name, cache_folder="app/backend/embedding/cache_embedding_model/")

