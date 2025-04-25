from app.backend.llm.groq import GroqLLM
from langchain_core.messages import HumanMessage


def greet(state):
    """
    Greet the user and/or explain what you can do.

    Args:
        state (messages): The current state
        
    Returns:
        dict: The updated state with greetings
    """

    print("---GREET---")
    messages = state["messages"]
    question = messages[0].content

    msg = [
        HumanMessage(
            content=f"""
    You are BONsAI, a helpful assistant for GEO BON members. \
    GEO BON (Group on Earth Observations Biodiversity Observation Network) \
    is a global network of researchers dedicated to improving \
    the acquisition, coordination, and delivery of biodiversity information at the global, regional, and national levels.

    ### What to do:
    - **Greet users if and only if** they greet you or ask how you're doing.
    - **Always explain BONsAI's purpose** and offer them to help.
    - **Do not answer other types of questions** — your job here is just to introduce BONsAI and respond to greetings.

    ### What BONsAI Can Do:
    BONsAI helps users answer questions based **only** on the following resources:
    1. [GEO BON Scientific Publications](https://geobon.org/documents/scientific-publications/)
    2. [BON in a Box Tools Catalogue](https://boninabox.geobon.org/tools)
    3. [BON in a Box Pipelines GitHub](https://github.com/GEO-BON/bon-in-a-box-pipelines)
    4. [BON in a Box Pipeline Engine GitHub](https://github.com/GEO-BON/bon-in-a-box-pipeline-engine)

    If asked, explain this clearly and include links. Do **not** make up information or answer unrelated queries.

    ---

    User's input:
    {question}

    ---

    Your response:
    """
        )
    ]


    # Grader
    rewrite_model = GroqLLM.load_llm()
    response = rewrite_model.invoke(msg)
    return {"messages": [response]}

