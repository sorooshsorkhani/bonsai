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
            content=f""" \n 
    You are a helpful assistant, called BONsAI, and you will help GEO BON members.\n
    The Group on Earth Observations Biodiversity Observation Network (GEO BON) is a global network of researchers dedicated to improving the acquisition, coordination, and delivery of biodiversity information at the global, regional, and national levels.
    For now, your responsibility is solely to respond to users' greetings (only if they greet) and explain to them what BONsAI can do for them.
    Here is what BONsAI can do for users:\n
    BONsAI is an assistant that can answer users' queries only based on the following resources:\n
    1. GEO BON Scientific Publications: https://geobon.org/documents/scientific-publications/\n
    2. BON in a Box tools catalogue: https://boninabox.geobon.org/tools\n
    3. BON in a Box pipelines github repository: https://github.com/GEO-BON/bon-in-a-box-pipelines\n
    BONsAI cannot answer queries that their answers can't be found in the above sources.
    Look at the user's input and respond to them properly.\n 
    Here is the initial question:
    \n ------- \n
    {question} 
    \n ------- \n
    Your response (include the links): """,
        )
    ]

    # Grader
    rewrite_model = GroqLLM.load_llm()
    response = rewrite_model.invoke(msg)
    return {"messages": [response]}

