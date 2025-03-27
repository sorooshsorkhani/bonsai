# This code is moved from a jupyter notebook
# For now, execute the script just once to create github_documents.pkl

import os
import re
import pickle
from langchain_community.document_loaders import PyPDFDirectoryLoader

# paths
BON_AI_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
GEOBON_FOLDER = os.path.join(BON_AI_ROOT, "app/backend/files/GEO BON Publications/")
DATA_PATH = os.path.join(BON_AI_ROOT, "app/backend/data/paper_docs.pkl")

def load_geobon_papers():
    """Loads and processes PDF files, then saves them as a pickle file."""
    print(f"Loading PDFs from: {GEOBON_FOLDER}...")
    
    loader = PyPDFDirectoryLoader(GEOBON_FOLDER)
    paper_docs = loader.load()

    for doc in paper_docs:
        source_text = doc.metadata['source']
        match = re.search(r'GEO BON Publications/\d{4} - .*', source_text)

        if match:
            cleaned_source = match.group(0).replace("/", " - ").rstrip(".pdf")
            doc.metadata['source'] = cleaned_source

        match = re.match(r'GEO BON Publications - (\d{4}) - (.+)', doc.metadata['source'])
        if match:
            doc.metadata['source_type'] = "GEO BON Publications"
            doc.metadata['year'] = int(match.group(1))
            doc.metadata['publication_title'] = match.group(2)

        doc.metadata = {key: doc.metadata.get(key) for key in ['source', 'source_type', 'year', 'publication_title', 'total_pages', 'page']}

    # Ensure the data directory exists before saving
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

    print(f"Saving loaded documents to: {DATA_PATH}...")
    with open(DATA_PATH, "wb") as file:
        pickle.dump(paper_docs, file)

    print("Processing completed and data saved.")


if __name__ == "__main__":
    load_geobon_papers()
