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
    Generates queries according to user's input and the history to retrieve documents.

    Args:
        state (user_queries): The current user_queries state
        state (summary): The current conversation summary state
        state (documents): The current documents state
        state (gen_queries): The generated queries state

    Returns:
        list: A list of generated queries
    """

    print("---GENERATE QUERIES---")


    # LLM
    query_generator_model = GroqLLM.load_llm()

    # Prompt
    prompt = PromptTemplate(
            template="""
        You are an expert query generator. \
            Your job is to look at the user's new query, user's past queries (if any) and the summary of the recent conversation (if any) with BONsAI. \
            find out *only* what the user is trying to find now, and then output 3 concise, keyword‑only search queries to be used for retrieval with similarity search.

        User's past queries (if any):
        <past_queries>
            {past_queries}
        </past_queries>

        The summary of recent conversation (if any):
        <conversation_summary>
            {prev_summary}
        </conversation_summary>

        User's new query:
        {last_query}

        Instructions:
        - Extract each distinct information need from the new query.
        - For each need, output a single phrase of keywords (no full sentences).
        - Do *not* repeat or paraphrase the past conversation.
        - Do *not* include explanations, numbering, bullets, or any text other than the queries.
        - Output exactly one query per line, maximum three lines.

        Generated queries:""",
            input_variables=["past_queries", "prev_summary", "last_query"],
    )

    # Chain
    output_parser = LineListOutputParser()
    query_generator_chain = prompt | query_generator_model | output_parser

    messages = state["messages"]
    #query = messages[0].content
    query = state['question']
    docs = state['documents']

    generated_queries = query_generator_chain.invoke({"query": query, "context": format_docs(docs)})
    print(generated_queries)
    
    return {"messages": generated_queries}