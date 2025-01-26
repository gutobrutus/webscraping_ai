import os

from langchain_openai import ChatOpenAI
from decouple import config

def create_openai_llm(model_name, temperature):
    """
    Function for OpenAI provider.
    """
    os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
    )
