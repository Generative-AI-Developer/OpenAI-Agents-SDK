import os
from dotenv import load_dotenv
from agents import Agent, Runner,  set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from litellm import completion
set_tracing_disabled(disabled=True)

MODEL = 'gemini/gemini-2.0-flash'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def main(model:str, api_key:str):
    agent = Agent(
        name = "Assistant",
        instructions = "You are a helpful assistant.",
        model = LitellmModel(model = model, api_key = api_key)
    )

    resutl = Runner.run_sync(agent, "What is the capital of Paksitan?")
    print(resutl.final_output)
main(model = MODEL, api_key = GEMINI_API_KEY)    
   

