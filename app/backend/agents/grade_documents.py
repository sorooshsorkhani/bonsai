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

    Args:
        state (messages): The current messages state
        state (documents): The current documents state

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
    relevance_prompt = PromptTemplate(
        template="""
        You are an expert relevance grader.

        **Task:** Decide whether the <context> passage is topically relevant to the <query>.  
        A passage is **relevant** if **any** of the following hold  
        • overlaps in subject area, discipline, goal, or problem domain  
        • shares key entities, concepts, or synonyms (even if wording differs)  
        • answers, explains, or supplements part of the user’s need  
        It does **not** have to fully answer the query or match every keyword.

        --------------------
        <context>
        {context}
        </context>

        <query>
        {query}
        </query>
        --------------------

        **Output rules**  
        1. Think silently about semantic and keyword overlap.  
        2. Output exactly one word on its own line:  
        • `yes`  – context is relevant  
        • `no`   – context is not relevant  
        (No quotation marks, additional text, or punctuation.)

        Begin your silent reasoning now. Then output your single-word verdict:
        """,
            input_variables=["context", "query"],
    )

    # Chain
    relevance_chain = relevance_prompt | llm_with_relevance

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
        state (messages): The current messages state
        state (documents): The current documents state

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
    sufficiency_prompt = PromptTemplate(
        template="""
        You are an expert sufficiency grader.

        **Task:** Decide whether the <context> passage by itself contains *enough* information to directly and completely answer the <query>.  
        A passage is **sufficient** if:

        • Every part of the query can be answered from the passage alone  
        • No key facts, steps, or definitions are missing  
        • A well-informed answer could be written without consulting additional sources

        If the passage is only partially helpful, leaves major gaps, or you would still “need to look something up,” it is **not** sufficient.

        --------------------
        <context>
        {context}
        </context>

        <query>
        {query}
        </query>
        --------------------

        **Output rules**  
        1. Think silently about completeness and coverage.  
        2. Output exactly one word on its own line:  
        • `yes`  – context is sufficient  
        • `no`   – context is not sufficient  
        (No other text, punctuation, or quotation marks.)

        Begin your silent reasoning now. Then output your single-word verdict:
        """,
            input_variables=["context", "query"],
    )

    # Chain
    sufficiency_chain = sufficiency_prompt | llm_with_sufficiency

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

