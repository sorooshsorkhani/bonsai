# This code is moved from a jupyter notebook
# For now, execute the script just once to create github_documents.pkl

import os
import json
import pickle
from dotenv import load_dotenv
from langchain_community.document_loaders import GithubFileLoader

# Load environment variables
load_dotenv()
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN") # will expire in 30 days from creation

# Define absolute paths
BON_AI_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DATA_PATH = os.path.join(BON_AI_ROOT, "app/backend/data/github_docs.pkl")

# Allowed extensions and folders
ALLOWED_EXTENSIONS = [".yml", ".md"]
ALLOWED_FOLDERS = ["pipelines/", "scripts/"]

def load_github_files(repo: str, branch: str, extensions: list, folders: list):
    """Loads GitHub files based on allowed extensions and folders."""
    loader = GithubFileLoader(
        repo=repo,
        branch=branch,
        access_token=GITHUB_ACCESS_TOKEN,
        github_api_url="https://api.github.com",
        file_filter=lambda file_path: (
            any(file_path.endswith(ext) for ext in extensions) and 
            any(file_path.startswith(folder) for folder in folders)
        ),
    )
    return loader.load()

def process_github_documents(documents):
    """Processes GitHub document metadata."""
    for doc in documents:
        doc.metadata["source"] = doc.metadata["source"].replace("api.github.com", "github.com")
        doc.metadata["source_type"] = "BON in a Box Pipelines GitHub"
    return documents

def load_and_process_json(repo: str, branch: str, folders: list):
    """Loads JSON files and extracts metadata section."""
    loader = GithubFileLoader(
        repo=repo,
        branch=branch,
        access_token=GITHUB_ACCESS_TOKEN,
        github_api_url="https://api.github.com",
        file_filter=lambda file_path: (
            file_path.endswith(".json") and any(file_path.startswith(folder) for folder in folders)
        ),
    )
    json_documents = loader.load()
    processed_json_docs = []

    for doc in json_documents:
        doc.metadata["source"] = doc.metadata["source"].replace("api.github.com", "github.com")
        
        try:
            data = json.loads(doc.page_content)
            if "metadata" in data:
                doc.page_content = json.dumps(data["metadata"], indent=4)
                processed_json_docs.append(doc)
        except json.JSONDecodeError:
            pass  # Ignore invalid JSON files
    
    return processed_json_docs

def save_pickle(data, path):
    """Saves data to a pickle file."""
    with open(path, "wb") as file:
        pickle.dump(data, file)

def main():
    repo_name = "GEO-BON/bon-in-a-box-pipelines"
    branch_name = "main"

    # Load and process GitHub files
    github_documents = load_github_files(repo_name, branch_name, ALLOWED_EXTENSIONS, ALLOWED_FOLDERS)
    github_documents = process_github_documents(github_documents)

    # Load and process JSON files
    json_documents = load_and_process_json(repo_name, branch_name, ALLOWED_FOLDERS)
    github_documents.extend(json_documents)

    # Save final pickle file
    save_pickle(github_documents, DATA_PATH)
    print(f"Saved {len(github_documents)} documents to {DATA_PATH}")

if __name__ == "__main__":
    main()
