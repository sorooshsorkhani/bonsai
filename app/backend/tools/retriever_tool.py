from langchain.tools.retriever import create_retriever_tool
from app.backend.retrievers.retriever_factory import RetrieverFactory

class RetrieverTool:
    """Creates and returns a retriever tool instance."""

    @staticmethod
    def get_retriever(mmr_k: int = 2, self_query_k: int = 2):
        """Creates and returns a retriever tool instance with default parameters."""

        mmr_retriever = RetrieverFactory.mmr_retriever(k=mmr_k)
        self_query_retriever = RetrieverFactory.self_query_retriever(k=self_query_k)

        merger_retriever = RetrieverFactory.merger_retriever([mmr_retriever, self_query_retriever])
        final_retriever = RetrieverFactory.compression_retriever(base_retriever=merger_retriever)

        description = "Search and return information about biodiversity, \
            GEO BON, BON in a Box (BiaB) tools and BiaB pipelines. BiaB pipelines GitHub repository \
            is for Mapping Kunming-Montreal Global Biodiversity Framework indicators and their uncertainty."

        return create_retriever_tool(
            final_retriever,
            "retrieve_information",
            description=description,
        )

