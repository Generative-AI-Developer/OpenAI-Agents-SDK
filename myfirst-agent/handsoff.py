# 

import os

from dotenv import load_dotenv
from agents import Agent, Runner,  set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
set_tracing_disabled(disabled=True)

MODEL = 'gemini/gemini-2.0-flash'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def main():
    agent = Agent(
        name = "Assistant",
        instructions = "You are a helpful assistant.",
        model = LitellmModel(model = MODEL, api_key = GEMINI_API_KEY)
    )

    result = Runner.run_sync(agent, "What is the capital of Paksitan?")
    print(result.final_output)

if __name__ == "__main__":
    main() 
   
