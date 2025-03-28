from app.backend.llm.groq import GroqLLM
from langchain_core.output_parsers import StrOutputParser

def rag(state):
    """
    Generate answer based on retrieved documents

    Args:
        state (messages): The current state

    Returns:
         dict: The updated state with the final response
    """
    print("---GENERATE---")
    messages = state["messages"]
    question = messages[0].content
    last_message = messages[-1]

    docs = last_message.content

    # Prompt
    prompt = """You are an assistant, called BON AI, for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Use three sentences maximum and keep the answer concise.
    Question: {question} 
    Context: {context} 
    Answer:
    """

    # LLM
    rag_model = GroqLLM.load_llm()

    # Post-processing
    def format_docs(docs):
        return "\n\n".join(
        (f"Document:\nReference: {doc.metadata}\nContent: {doc.page_content}")
        for doc in docs
    )

    # Chain
    rag_chain = prompt | rag_model | StrOutputParser()

    # Run
    response = rag_chain.invoke({"context": format_docs(docs), "question": question})
    return {"messages": [response]}

