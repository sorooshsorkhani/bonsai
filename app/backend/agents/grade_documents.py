from app.backend.llm.groq import GroqLLM
from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate

def format_docs(docs):
    serialized = "\n\n".join(
            (f"Document {i+1}:\n\Metadata: {doc.metadata}\nContent: {doc.page_content}")
            for i, doc in enumerate(docs)
        )
    return serialized

def grade_relevance(state) -> Literal["grade_sufficiency", "greetings"]:
    """
    Determines whether the retrieved documents are relevant to the query.

    Args:`
        state (messages): The current state

    Returns:
        str: A decision for whether the documents are relevant or not
    """

    print("---CHECK RELEVANCE---")

    # Data model
    class grade(BaseModel):
        """Binary score for relevance check."""

        binary_score: str = Field(description="Relevance score 'yes' or 'no'")

    # LLM
    relevance_model = GroqLLM.load_llm()

    # LLM with tool and validation
    llm_with_relevance = relevance_model.with_structured_output(grade)

    # Prompt
    prompt = PromptTemplate(
        template="""You are a grader assessing relevance of retrieved documents to a user query. \n 
        Here is the retrieved documents: \n\n {context} \n\n
        Here is the user query: {query} \n
        If the documents contain keyword(s) or semantic meaning related to the user query, grade it as relevant. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the query.""",
        input_variables=["context", "query"],
    )

    # Chain
    relevance_chain = prompt | llm_with_relevance

    messages = state["messages"]
    query = messages[0].content
    #last_message = messages[-1]
    #docs = last_message.content
    docs = state['documents']

    scored_result = relevance_chain.invoke({"query": query, "context": format_docs(docs)})

    score = scored_result.binary_score

    if score == "yes":
        print("---DECISION: DOCS RELEVANT---")
        return "grade_sufficiency"

    else:
        print("---DECISION: DOCS NOT RELEVANT---")
        print(score)
        return "greetings"


def grade_sufficiency(state) -> Literal["rag", "generate_queries"]:
    """
    Determines whether the retrieved documents are sufficient to answer the query.

    Args:
        state (messages): The current state

    Returns:
        str: A decision for whether the documents are sufficient or not
    """

    print("---CHECK SUFFICIENCY---")

    # Data model
    class grade(BaseModel):
        """Binary score for sufficiency check."""

        binary_score: str = Field(description="Sufficiency score 'yes' or 'no'")

    # LLM
    sufficiency_model = GroqLLM.load_llm()

    # LLM with tool and validation
    llm_with_sufficiency = sufficiency_model.with_structured_output(grade)

    # Prompt
    prompt = PromptTemplate(
        template="""You are a grader assessing sufficiency of retrieved documents to a user query. \n 
        Here is the retrieved documents: \n\n {context} \n\n
        Here is the user query: {query} \n
        If the documents sufficient to answer the user query and no additional context is needed, grade it as sufficient. \n
        Give a binary score 'yes' or 'no' score to indicate whether the documents are sufficient.""",
        input_variables=["context", "query"],
    )

    # Chain
    sufficiency_chain = prompt | llm_with_sufficiency

    messages = state["messages"]
    query = messages[0].content
    #last_message = messages[-1]
    #docs = last_message.content
    docs = state['documents']

    scored_result = sufficiency_chain.invoke({"query": query, "context": format_docs(docs)})

    score = scored_result.binary_score

    if score == "yes":
        print("---DECISION: DOCS SUFFICIENT---")
        return "rag"

    else:
        print("---DECISION: DOCS NOT SUFFICIENT---")
        print(score)
        return "generate_queries"

