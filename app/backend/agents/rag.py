from app.backend.llm.groq import GroqLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate


def rag(state):
    """
    Generate answer based on retrieved documents

    Args:
        state (messages): The current state
        
    Returns:
         dict: The updated state with the final response
    """
    print("---RAG---")
    messages = state["messages"]
    question = messages[0].content
    last_message = messages[-1]
    docs = last_message.content
    

    # Prompt
    prompt = PromptTemplate(
        template="""You are an assistant, called BON AI, for question-answering tasks.\n
        Use the following pieces of retrieved documents to answer the question.\n
        The documents contain metadata and content.\n
        If you don't know the answer, just say that you don't know.\n
        Use three sentences maximum and keep the answer concise.\n\n
        Question: {question}\n\n
        Documents:\n\n{context}\n\n
        Answer:""",
        input_variables=["context", "question"],
    )

    # LLM
    rag_model = GroqLLM.load_llm()

    # Chain
    rag_chain = prompt | rag_model | StrOutputParser()

    # Run
    response = rag_chain.invoke({"context": docs, "question": question})
    return {"messages": [response]}

