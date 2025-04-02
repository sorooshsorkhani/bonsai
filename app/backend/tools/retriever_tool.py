from langchain_core.tools import tool
from app.backend.retrievers.retriever_factory import RetrieverFactory


@tool(response_format="content")
def doc_retriever(query:str):
    """Retrieve information related to a query."""

    mmr_retriever = RetrieverFactory.mmr_retriever(k=2)
    self_query_retriever = RetrieverFactory.self_query_retriever(k=2)

    merger_retriever = RetrieverFactory.merger_retriever([mmr_retriever, self_query_retriever])
    final_retriever = RetrieverFactory.compression_retriever(base_retriever=merger_retriever)

    retrieved_docs = final_retriever.invoke(query)
    serialized = "\n\n".join(
        (f"Document {i+1}:\n\Metadata: {doc.metadata}\nContent: {doc.page_content}")
        for i, doc in enumerate(retrieved_docs)
    )

    return serialized
