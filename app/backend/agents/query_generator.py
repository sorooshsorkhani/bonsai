from app.backend.llm.groq import GroqLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import BaseOutputParser
from typing import List
from app.backend.tools.retriever_tool import doc_retriever

def format_docs(docs):
    serialized = "\n\n".join(
            (f"Document {i+1}:\n\Metadata: {doc.metadata}\nContent: {doc.page_content}")
            for i, doc in enumerate(docs)
        )
    return docs[0].page_content

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
        template="""You are an expert query generator. Your goal is to identify gaps in the provided context that prevent a complete answer to the user's query.\n
            Carefully compare the user's question and the provided context to see what information is missing.\n
            Only generate additional queries that would help fill in missing details — not repeat what is already known.\n\n
            Here is the context that is already seen (you should NOT generate queries to repeat this information):\n
            {context}\n\n
            Here is the user's query: {query}\n\n
            What is missing from the context that prevents a full answer to the user's query?\n
            Generate 1 to 3 focused and specific queries that would retrieve documents to fill in those gaps.\n\n
            Each query should be short, keyword-rich, and optimized for search in a vector database.\n
            ❗ Do NOT use full sentences. Use compact phrases or keywords.\n
            ❌ Do NOT include explanation or context.\n
            ✅ Only output the queries, separated by newlines.\n\n
            Additional queries:\n""",
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
    
    return {"messages": [generated_queries]}