import os

from langchain_groq import ChatGroq
from decouple import config

def create_groq_llm(model_name, temperature):
    """
    Function for Groq provider. 
    """
    os.environ['GROQ_API_KEY'] = config('GROQ_API_KEY')

    return ChatGroq(
        model=model_name,
        temperature=temperature,
    )
