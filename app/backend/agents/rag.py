from app.backend.llm.groq import GroqLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate


def format_docs(docs):
    serialized = "\n\n".join(
            (f"Metadata: {doc.metadata}\nContent: {doc.page_content}")
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
        You are BONsAI, an expert assistant specialized in biodiversity, GEO BON, and BON in a Box.

        Your task is to answer the user’s question **only using the information provided inside the <context> block below**. \
            This information is retrieved from a knowledge base and is not part of the conversation with the user.

        <context>
            {context}
        </context>

        Instructions:
        - Generate a **clear, comprehensive, and well-structured** answer based solely on the content inside the <context> block.
        - If there is no relevant information in the context to answer the question, respond with: **"Hmm, I'm not sure."** Do not guess or fabricate answers.
        - Use a **neutral, journalistic tone**—informative and unbiased.
        - When multiple documents provide relevant info, **synthesize them into a single coherent answer**.
        - **Do not repeat content** from different sources. Merge ideas where possible.
        - **Cite sources** using `[number]` format directly after the relevant sentence or paragraph. Only cite documents that are directly relevant.
        - Format your response using **markdown**, with **bullet points** and **headings** if appropriate, to ensure readability.
        - If different documents refer to different entities with the same name, write **separate answers for each**.

        At the end of your response, include a **References** section listing the documents you cited:
        - In the **References** section, **number each entry** in the order it was cited in your response, using the same numbers as in the citations (e.g., `[1]`, `[2]`, etc.).
        - Use the "source" from document metadata to reference.
        - Put each reference on a bullet point, in ascending order of their citation number (from 1 to ...).

        Repeat: Only use the information from the context. If nothing relevant is found, just say "Hmm, I'm not sure."

        \n\nQuestion: {question}\n\n
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

