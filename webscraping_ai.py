import argparse

from langchain.agents import AgentType, initialize_agent
from langchain_community.tools.playwright.utils import create_sync_playwright_browser
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from llm_factory import create_llm

# Function prompt file read
def read_prompt_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def main():
    # argparse config
    parser = argparse.ArgumentParser(description="AI-powered Web Scraping from a txt file containing the prompt using OpenAI or Groq")
    parser.add_argument('file_prompt', type=str, help="Path to the text file containing the prompt")
    parser.add_argument('model_provider', type=str, choices=['openai', 'groq'], help="Choose between 'openai' or 'groq' for LLM provider")
    
    # args for model llm
    parser.add_argument('--model_name', type=str, default='gpt-4o-mini', help="Model name (default: 'gpt-4o-mini')")
    parser.add_argument('--temperature', type=float, default=0.0, help="Model temperature (default: 0.0)")
    
    args = parser.parse_args()

    # Read file prompt
    prompt = read_prompt_from_file(args.file_prompt)

    llm = create_llm(args.model_provider, args.model_name, args.temperature)

    # Config browser and toolkit
    browser = create_sync_playwright_browser()
    toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=browser)
    tools = toolkit.get_tools()

    # Init agent with tools
    agent_chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    # Invoke agent with prompt
    result = agent_chain.invoke(input=prompt)

    # Print result
    print(result.get('output'))


if __name__ == "__main__":
    main()