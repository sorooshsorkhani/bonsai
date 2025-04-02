from app.backend.llm.groq import GroqLLM
from langchain_core.messages import HumanMessage


def rewrite(state):
    """
    Transform the query to produce a better question.

    Args:
        state (messages): The current state
        
    Returns:
        dict: The updated state with re-phrased question
    """

    print("---TRANSFORM QUERY---")
    messages = state["messages"]
    question = messages[0].content

    msg = [
        HumanMessage(
            content=f""" \n 
    Look at the input and try to reason about the underlying semantic intent / meaning. Rewrite an improved question and replace the initial one.\n 
    Here is the initial question:
    \n ------- \n
    {question} 
    \n ------- \n
    The improved question: """,
        )
    ]

    # Grader
    rewrite_model = GroqLLM.load_llm()
    response = rewrite_model.invoke(msg)
    return {"messages": [response]}

