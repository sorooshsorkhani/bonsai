from app.backend.tools.retriever_tool import get_retriever


test_retriever = get_retriever(mmr_k=1, self_query_k=1, response_format="content")
#print(test_retriever)

retrieved_docs = test_retriever.invoke("What is an EBV?")
print(retrieved_docs)