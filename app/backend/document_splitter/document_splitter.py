from langchain.text_splitter import RecursiveCharacterTextSplitter


def doc_splitter(docs, chunk_size=1500, chunk_overlap=500):
    """
    Splits a list of text documents into smaller chunks using RecursiveCharacterTextSplitter.
    
    Args:
        docs (list): List of text documents (strings).
        chunk_size (int): Maximum chunk size.
        chunk_overlap (int): Overlap between chunks.
    
    Returns:
        list: List of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunked_docs = []
    for doc in docs:
        chunked_docs.extend(text_splitter.split_text(doc))

    return chunked_docs
