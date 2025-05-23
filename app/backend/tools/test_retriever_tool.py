from app.backend.tools.retriever_tool import doc_retriever
#from langchain.retrievers.multi_query import MultiQueryRetriever

query = "BON in a Box pipeline assembly"

print("\n\nCustom retriever:\n\n")
summary, custom_retrieved_docs = doc_retriever.func(query)
print(custom_retrieved_docs)

