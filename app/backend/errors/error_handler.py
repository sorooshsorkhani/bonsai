import groq

def handle_groq_error(error):
    """
    Handles errors related to the groq library.

    Args:
        error (Exception): The exception raised by groq.
    
    Returns:
        str: A user-friendly error message.
    """
    if isinstance(error, groq.RateLimitError):
        print("A 429 status code was received; we should back off a bit.")
        return "[ERROR:RATE_LIMIT]"
    elif isinstance(error, groq.APIConnectionError):
        print("The server could not be reached")
        print(error.__cause__)  # Log the underlying issue
        return "[ERROR:The server could not be reached]"
    elif isinstance(error, groq.APIStatusError):
        print("Another non-200-range status code was received")
        print(error.status_code)
        print(error.response)
        return "[ERROR:Unexpected server response]"
    else:
        print("An unknown error occurred:", str(error))
        return "[ERROR:Unknown error]"
