# This code is moved from a jupyter notebook
# For now, execute the script just once to create github_documents.pkl

import os
import json
import pickle
from dotenv import load_dotenv
from langchain_community.document_loaders import GithubFileLoader

# Load environment variables
load_dotenv(override=True)
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN") # will expire in 30 days (on June 20, 2025)


# Define absolute paths
BONSAI_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DATA_PATH = os.path.join(BONSAI_ROOT, "app/backend/data/github_docs.pkl")

def load_github_files(repo: str, branch: str, extensions: list=[], folders: list=[]):
    """Loads GitHub files based on allowed extensions and folders."""
    loader = GithubFileLoader(
        repo=repo,
        branch=branch,
        access_token=GITHUB_ACCESS_TOKEN,
        github_api_url="https://api.github.com",
        file_filter=lambda file_path: (
            (not extensions or any(file_path.endswith(ext) for ext in extensions)) and
            (not folders or any(file_path.startswith(folder) for folder in folders))
        ),
    )
    return loader.load()

def process_github_documents(documents):
    """Processes GitHub document metadata."""
    for doc in documents:
        doc.metadata["source"] = doc.metadata["source"].replace("api.github.com", "github.com")
        doc.metadata["document_category"] = "BON in a Box Pipelines GitHub"

        # New line for metadata optimization purposes. Eliminating extra metadata fields
        doc.metadata = {key: doc.metadata.get(key) for key in ['source', 'document_category']}
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

    # Load and process the pipelines repo
    pipeline_repo_name = "GEO-BON/bon-in-a-box-pipelines"
    pipeline_branch_name = "main"
    # Load and process [".yml", ".md", ".Rmd"] files
    pipeline_documents = load_github_files(pipeline_repo_name, pipeline_branch_name, extensions=[".yml", ".md", ".Rmd"], folders=["pipelines/", "scripts/"])
    pipeline_documents = process_github_documents(pipeline_documents)
    # Load and process JSON files
    json_documents = load_and_process_json(pipeline_repo_name, pipeline_branch_name, folders=["pipelines/", "scripts/"])
    pipeline_documents.extend(json_documents)


    # Load and process the pipeline engine repo
    engine_repo_name = "GEO-BON/bon-in-a-box-pipeline-engine"
    engine_branch_name = "edge"
    engine_documents = []
    # Load and process ".yml" files
    engine_documents1 = load_github_files(engine_repo_name, engine_branch_name, extensions=[".yml"], folders=["script-stubs/"])
    engine_documents1 = process_github_documents(engine_documents1)
    # Load and process the ".yaml" file
    engine_documents2 = load_github_files(engine_repo_name, engine_branch_name, extensions=[".yaml"], folders=["script-server/api/"])
    engine_documents2 = process_github_documents(engine_documents2)
    # Load and process ".md", ".qmd" files
    engine_documents3 = load_github_files(engine_repo_name, engine_branch_name, extensions=[".md", ".qmd"])
    engine_documents3 = process_github_documents(engine_documents3)
    # Combine the engine docs
    engine_documents.extend(engine_documents1)
    engine_documents.extend(engine_documents2)
    engine_documents.extend(engine_documents3)


    # Combine the documents from all repositories
    github_documents = []
    github_documents.extend(pipeline_documents + engine_documents)

    # Save final pickle file
    save_pickle(github_documents, DATA_PATH)
    print(f"Saved {len(github_documents)} documents to {DATA_PATH}")

if __name__ == "__main__":
    main()
