from openai_llm import create_openai_llm
from groq_llm import create_groq_llm

def create_llm(model_type, model_name, temperature):
    """
    Factory for LLMs (OpenAI ou Groq).
    """
    if model_type == "openai":
        return create_openai_llm(model_name, temperature)
    elif model_type == "groq":
        return create_groq_llm(model_name, temperature)
    else:
        raise ValueError("Invalid LLM provider. Valid options: 'openai' or 'groq'.")
