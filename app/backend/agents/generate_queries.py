from app.backend.llm.groq import GroqLLM
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import BaseOutputParser
from typing import List

def format_docs(docs):
    serialized = "\n\n".join(
            (f"Document {i+1}:\n\Metadata: {doc.metadata}\nContent: {doc.page_content}")
            for i, doc in enumerate(docs)
        )
    return docs[0]

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

    # Data model
    class query_list(BaseModel):
        """List of generated queries."""

        queries: list = Field(description="List of generated queries (max 3) like ['query_text1', 'query_text2','query_text3']")

    # LLM
    query_generator_model = GroqLLM.load_llm()

    # Prompt
    prompt = PromptTemplate(
        template="""You are an expert query generator.
        The provided context is not sufficient to answer the user's query.
        Understand what the user is looking for and why the context is not sufficient to answer the user's query.\n
        Then, generate 1 to 3 queries to be used for retrieving additonal documents to fill the gap in the context to answer the user's query.\n
        Here is the retrieved documents: \n\n {context} \n\n
        Here is the user query: {query} \n
        Provide these additional queries separated by newlines.\n
        Additional queries:
        """,
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
    
    return generated_queries