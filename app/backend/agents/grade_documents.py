from app.backend.llm.groq import GroqLLM
from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate


def grade_docs(state) -> Literal["rag", "rewrite"]:
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
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
    grade_model = GroqLLM.load_llm()

    # LLM with tool and validation
    llm_with_tool = grade_model.with_structured_output(grade)

    # Prompt
    prompt = PromptTemplate(
        template="""You are a grader assessing relevance of retrieved documents to a user question. \n 
        Here is the retrieved documents: \n\n {context} \n\n
        Here is the user question: {question} \n
        If the documents contain keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.""",
        input_variables=["context", "question"],
    )

    # Chain
    chain = prompt | llm_with_tool

    messages = state["messages"]
    question = messages[0].content
    last_message = messages[-1]
    docs = last_message.content

    scored_result = chain.invoke({"question": question, "context": docs})

    score = scored_result.binary_score

    if score == "yes":
        print("---DECISION: DOCS RELEVANT---")
        return "rag"

    else:
        print("---DECISION: DOCS NOT RELEVANT---")
        print(score)
        return "rewrite"
