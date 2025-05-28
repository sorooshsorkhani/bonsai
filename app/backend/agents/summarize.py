from app.backend.llm.groq import GroqLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

def summarizer(state):
    """
    Generate a summary of the whole conversation

    Args:
        state (messages): The current state
        
    Returns:
         dict: The updated state with a summary
    """
    print("---SUMMARIZE---")
    messages = state["messages"]
    #question = messages[0].content
    question = state['question']
    docs = state['documents']
    

    # Prompt
    prompt = PromptTemplate(
        template="""
        You are an expert summarizer. Your task is to summarize user's conversation with a chatbot called BONsAI.
        Given the user’s questions, the previous compact summary of BONsAI’s replies, and BONsAI’s most recent answer, \
            produce a single concise summary that preserves all user intents, key answers, and next-steps so BONsAI can continue without re-reading the full history.

        Inputs:
        <questions>
            {questions}
        </questions>

        <prev_summary>
            {prev_summary}
        </prev_summary>

        <last_response>
            {last_response}
        </last_response>

        Instructions:
        - Cover the entire dialogue (including the last_response).  
        - Highlight user goals, BONsAI’s solutions, and any outstanding tasks.  
        - Use markdown (either 2–4 bullet points or a short paragraph).  
        - Maximum 80 words.  

        ### Summary:
        """,
            input_variables=["questions", "prev_summary", "last_response"],
    )


    # LLM
    rag_model = GroqLLM.load_llm()

    # Chain
    rag_chain = prompt | rag_model | StrOutputParser()

    # Run
    response = rag_chain.invoke({"context": format_docs(docs), "question": question})
    return {"messages": [response]}