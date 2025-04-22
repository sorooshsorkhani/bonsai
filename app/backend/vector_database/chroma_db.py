# This code is moved from a jupyter notebook
# For now, execute the script just once to create and persist the vectordb

import os
import pickle
from langchain_chroma import Chroma
from app.backend.embedding.hf_embedding import load_embedding
from app.backend.document_splitter.document_splitter import doc_splitter

# Get the absolute path of the current script
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

# Determine the embedding model
embedding_mode_name = "static-similarity-mrl-multilingual-v1"

# Define the persist directory inside the same folder as the script
PERSIST_DIRECTORY = os.path.join(CURRENT_DIR, "vectordb-"+embedding_mode_name)
DATA_PATH = os.path.join(CURRENT_DIR, "../data")


def load_pickle(file_path):
    """Loads and returns data from a pickle file."""
    with open(file_path, "rb") as file:
        return pickle.load(file)


def initialize_vectordb():
    """
    Initializes and persists the Chroma vector database only if it does not already exist.
    """
    if os.path.exists(PERSIST_DIRECTORY) and os.listdir(PERSIST_DIRECTORY):
        print(f"Vector database already exists at: {PERSIST_DIRECTORY}")
        return
    
    # Load pickle files
    github_docs = load_pickle(DATA_PATH+"/github_docs.pkl")
    tools_docs = load_pickle(DATA_PATH+"/tools_docs.pkl")
    paper_docs = load_pickle(DATA_PATH+"/paper_docs.pkl")  # This one needs further processing

    # Split paper_docs using doc_splitter
    paper_docs_splits = doc_splitter(paper_docs)
    splits = paper_docs_splits + github_docs + tools_docs

    # Load embedding
    embedding = load_embedding(model_name=embedding_mode_name)

    # Create and persist the vector database
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=PERSIST_DIRECTORY
    )

    print(f"Vector database successfully created in: {PERSIST_DIRECTORY}")


def load_vectordb():
    """
    Load the vector database
    """
    vectordb = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=load_embedding(model_name=embedding_mode_name)
    )
    return vectordb


if __name__ == "__main__":
    initialize_vectordb()
