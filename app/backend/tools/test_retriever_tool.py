from app.backend.tools.retriever_tool import doc_retriever
from langchain.retrievers.multi_query import MultiQueryRetriever

query = "What is an EBV?"

print("\n\nCustom retriever:\n\n")
custom_retrieved_docs = doc_retriever.invoke(query)
print(custom_retrieved_docs)

