import os
import requests

from langchain_groq import ChatGroq
from langchain_core.rate_limiters import InMemoryRateLimiter
from decouple import config

def get_max_completion_tokens(model_name):
    """
    Function to get the value of 'max_completion_tokens' for a specific model via the Groq API.
    """
    url = "https://api.groq.com/openai/v1/models"
    headers = {
        "Authorization": f"Bearer {config('GROQ_API_KEY')}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        models = response.json()
        for model in models['data']:
            if model['id'] == model_name:
                return model['context_window']
        raise ValueError(f"Model {model_name} not found in Groq API.")
    else:
        raise Exception(f"Error to access Groq API: {response.status_code} - {response.text}")

def create_groq_llm(model_name, temperature):
    """
    Function for Groq provider. 
    """
    os.environ['GROQ_API_KEY'] = config('GROQ_API_KEY')

    max_tokens = get_max_completion_tokens(model_name)

    rate_limiter = InMemoryRateLimiter(
        requests_per_second=0.1,  # <-- Super slow! We can only make a request once every 10 seconds!!
        check_every_n_seconds=0.1,  # Wake up every 100 ms to check whether allowed to make a request,
        max_bucket_size=10,  # Controls the maximum burst size.
    )

    return ChatGroq(
        model=model_name,
        temperature=temperature,
        max_completion_tokens=max_tokens,
        streaming=False,
        rate_limiter=rate_limiter,
    )
