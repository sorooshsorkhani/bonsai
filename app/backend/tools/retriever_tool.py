from langchain_core.tools import tool
from app.backend.retrievers.retriever_factory import RetrieverFactory
from langchain_core.documents import Document


@tool(response_format="content_and_artifact")
def doc_retriever(query:str):
    """Retrieve information related to a query."""

    mmr_retriever = RetrieverFactory.mmr_retriever(k=2)
    self_query_retriever = RetrieverFactory.self_query_retriever(k=2)

    merger_retriever = RetrieverFactory.merger_retriever([mmr_retriever, self_query_retriever])
    final_retriever = RetrieverFactory.compression_retriever(base_retriever=merger_retriever)

    retrieved_docs = final_retriever.invoke(query)
    # strip off any internal state/embeddings and return plain Document 
    clean_docs = [
        Document(page_content=doc.page_content, metadata=doc.metadata)
        for doc in retrieved_docs
    ]
    
    # first element is the user‑facing content (can be empty, or a simple summary)
    # second element is the actual list of Documents we want as .artifact
    summary = f"Retrieved {len(clean_docs)} documents."
    return summary, clean_docs
