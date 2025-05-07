#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Name: retriever_factory.py
Description: A factory class to construct various retrievers.
"""

from langchain.retrievers import MergerRetriever, ContextualCompressionRetriever
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_community.document_transformers import EmbeddingsRedundantFilter, LongContextReorder
from langchain.retrievers.document_compressors import LLMChainExtractor, DocumentCompressorPipeline
from app.backend.retrievers.metadata_info import DOCUMENT_CONTENT_DESCRIPTION, METADATA_FIELD_INFO
from app.backend.embedding.hf_embedding import load_embedding
from app.backend.vector_database import chroma_db
from app.backend.llm.groq import GroqLLM

class RetrieverFactory:
    """
    A factory class to create various retrievers like MMR, Self Query, Merger, and Compression retrievers.
    """

    @staticmethod
    def mmr_retriever(vectordb=chroma_db.load_vectordb(), k: int = 2):
        """
        Create a Maximal Marginal Relevance (MMR) Retriever.

        Parameters:
        - vectordb: The vector database to retrieve documents from.
        - k (int, optional): Number of documents to retrieve. Default is 3.

        Returns:
        - Retriever: A retriever using the MMR strategy to balance relevance and diversity.
        """
        return vectordb.as_retriever(search_type="mmr", search_kwargs={"k": k})


    @staticmethod
    def self_query_retriever(llm = GroqLLM.load_llm(model="llama-3.3-70b-versatile"), vectordb=chroma_db.load_vectordb(), k: int = 2):
        """
        Create a Self-Query Retriever that formulates queries based on user input.

        Parameters:
        - llm: The language model used for query generation.
        - vectordb: The vector database to retrieve documents from.
        - k (int, optional): Number of documents to retrieve. Default is 4.

        Returns:
        - SelfQueryRetriever: A retriever that dynamically constructs queries.
        """
        return SelfQueryRetriever.from_llm(
            llm,
            vectordb,
            document_contents=DOCUMENT_CONTENT_DESCRIPTION,
            metadata_field_info=METADATA_FIELD_INFO,
            verbose=True,
            fix_invalid=True,
            search_kwargs={"k": k},
            use_original_query=False
        )


    @staticmethod
    def merger_retriever(list_of_retrievers):
        """
        Merge multiple retrievers into a single retriever.

        Parameters:
        - list_of_retrievers : List[BaseRetriever]
            A list of LangChain retriever instances to merge.

        Returns:
        - MergerRetriever: A retriever that merges results from all provided retrievers.

        Raises:
        - ValueError: If no retrievers are provided.
        """
        if not list_of_retrievers:
            raise ValueError("You must provide at least one retriever.")
        return MergerRetriever(retrievers=list_of_retrievers)


    @staticmethod
    def compression_retriever(embedding=load_embedding(), llm=GroqLLM.load_llm(), base_retriever=None):
        """
        Create a Contextual Compression Retriever to filter and reorder retrieved documents.

        Parameters:
        - embedding: The embedding model used for redundancy filtering.
        - llm: The language model used for content extraction.
        - base_retriever: The initial retriever providing documents before compression.

        Returns:
        - ContextualCompressionRetriever: A retriever that enhances relevance by compressing and reordering retrieved documents.
        """
        if base_retriever is None:
            raise ValueError("base_retriever in compression_retriever cannot be None. Please provide a valid retriever.")
    
        redundant_filter = EmbeddingsRedundantFilter(embeddings=embedding)
        reordering = LongContextReorder()
        #llm_compressor = LLMChainExtractor.from_llm(llm=GroqLLM.load_llm("llama3-8b-8192"))

        pipeline = DocumentCompressorPipeline(transformers=[redundant_filter, reordering]) # , llm_compressor

        return ContextualCompressionRetriever(base_compressor=pipeline, base_retriever=base_retriever)
