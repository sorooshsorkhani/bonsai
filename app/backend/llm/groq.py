import os
from dotenv import load_dotenv
import getpass
from langchain_groq import ChatGroq

class GroqLLM:
    # Load environment variables
    load_dotenv(override=True)

    # Set the API key if not already set
    if not os.environ.get("GROQ_API_KEY"):
        print("Couldn't read Groq API Key")
        os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for Groq: ")

    # List of Groq models (in order of ranking)
    GROQ_MODELS = [
        'llama-3.3-70b-versatile',                       # 0
        'meta-llama/llama-4-maverick-17b-128e-instruct', # 1
        'meta-llama/llama-4-scout-17b-16e-instruct',     # 2
        'llama-3.1-8b-instant',                          # 3
        'llama3-8b-8192',                                # 4
        'llama-guard-3-8b'                               # -1
    ]

    @staticmethod
    def load_llm(model: str = GROQ_MODELS[2], temperature:int = 0, streaming:bool = True):
        """Load the model based on the provided name or use default (llama-3.3-70b-versatile)."""
        if model not in GroqLLM.GROQ_MODELS:
            available_models = ",\n".join(GroqLLM.GROQ_MODELS)  # Join available models into a string
            raise ValueError(f"Model '{model}' not found in available models. Available models are: {available_models}")
        
        # Initialize and return the selected model
        return ChatGroq(model=model, temperature=temperature, streaming=streaming)

# Define the function that will be called when executing the script
def load_and_print_models():
    """Load specific models and print them."""
    try:
        llama70b = GroqLLM.load_llm(model="llama-3.3-70b-versatile")
        llama8b = GroqLLM.load_llm(model="llama-3.1-8b-instant")
        print(f"Loaded models: {llama70b.model}, {llama8b.model}")
    except ValueError as e:
        print(e)

# Call the function only when this script is executed directly
if __name__ == "__main__":
    load_and_print_models()


