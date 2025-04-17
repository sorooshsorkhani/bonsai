from app.backend.llm.groq import GroqLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate


def format_docs(docs):
    serialized = "\n\n".join(
            (f"Document {i+1}:\n\Metadata: {doc.metadata}\nContent: {doc.page_content}")
            for i, doc in enumerate(docs)
        )
    return serialized


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
    #last_message = messages[-1]
    #docs = last_message.content
    docs = state['documents']
    

    # Prompt
    prompt = PromptTemplate(
        template="""\
        You are an expert assistant called BONsAI, tasked with answering any question \
        about biodiversity, GEO BON and BON in a Box.

        Generate a comprehensive and informative answer of 120 words or less for the \
        given question based solely on the provided retrieved documents (metadata and content). You must \
        only use information from the provided retrieved documents. Use an unbiased and \
        journalistic tone. Combine retrieved documents together into a coherent answer. Do not \
        repeat text. Cite retrieved documents using [$number:source(complete name of it)] notation. Only cite the most \
        relevant documents that answer the question accurately. Place these citations at the end \
        of the sentence or paragraph that reference them - do not put them all at the end. If \
        different documents refer to different entities within the same name, write separate \
        answers for each entity.

        You should use bullet points in your answer for readability. Put citations where they apply
        rather than putting them all at the end.

        If there is nothing in the context relevant to the question at hand, just say "Hmm, \
        I'm not sure." Don't try to make up an answer.

        Anything between the following `context`  html blocks is retrieved from a knowledge \
        bank, not part of the conversation with the user. 

        <context>
            {context} 
        <context/>

        REMEMBER: If there is no relevant information within the context, just say "Hmm, I'm \
        not sure." Don't try to make up an answer. Anything between the preceding 'context' \
        html blocks is retrieved from a knowledge bank, not part of the conversation with the \
        user.\
        \n\n Question: {question}\n\n
        Answer:
        """,
        input_variables=["context", "question"],
    )

    # LLM
    rag_model = GroqLLM.load_llm()

    # Chain
    rag_chain = prompt | rag_model | StrOutputParser()

    # Run
    response = rag_chain.invoke({"context": format_docs(docs), "question": question})
    return {"messages": [response]}

