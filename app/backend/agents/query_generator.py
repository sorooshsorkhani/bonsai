from app.backend.llm.groq import GroqLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import BaseOutputParser
from typing import List
from app.backend.tools.retriever_tool import doc_retriever

def format_docs(docs: List) -> str:

    return "\n\n".join(
        f"Document {i+1}:\nMetadata: {doc.metadata}\nContent: {doc.page_content}"
        for i, doc in enumerate(docs)
    )

class LineListOutputParser(BaseOutputParser[List[str]]):
    """Output parser for a list of lines."""

    def parse(self, text: str) -> List[str]:
        lines = text.strip().split("\n")
        return list(filter(None, lines))  # Remove empty lines

def generate_queries(state):
    """
    Generates additional queries to retrieve more documents to enrich the context.

    Args:
        state (messages): The current messages state
        state (documents): The current documents state

    Returns:
        list: A list of queries
    """

    print("---GENERATE QUERIES---")


    # LLM
    query_generator_model = GroqLLM.load_llm()

    # Prompt
    prompt = PromptTemplate(
            template="""
        You are an expert query generator. Your job is to look at what the user asked and what their retrieved documents already contain, find *only* the missing pieces needed to fully answer the question, and then output 1–3 concise, keyword‑only search queries to fill those gaps.

        Context (don’t repeat anything already here):
        <context>
            {context}
        </context>

        User question:
        {query}

        Instructions:
        – Identify up to three distinct facts or topics that are *not* present in the context but are needed to answer the user.
        – For each, write one short phrase of keywords (no full sentences).
        – Do *not* repeat or paraphrase the context.
        – Do *not* include explanations, numbering, bullets, or any text other than the queries.
        – Output exactly one query per line, maximum three lines.

        Additional queries:""",
            input_variables=["context", "query"],
    )

    # Chain
    output_parser = LineListOutputParser()
    query_generator_chain = prompt | query_generator_model | output_parser

    messages = state["messages"]
    query = messages[0].content
    #last_message = messages[-1]
    #docs = last_message.content
    docs = state['documents']

    generated_queries = query_generator_chain.invoke({"query": query, "context": format_docs(docs)})
    print(generated_queries)
    
    return {"messages": generated_queries}