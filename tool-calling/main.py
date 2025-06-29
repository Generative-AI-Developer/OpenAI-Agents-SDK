import os

from dotenv import load_dotenv
from agents import Agent, Runner,  set_tracing_disabled, function_tool
from agents.extensions.models.litellm_model import LitellmModel

set_tracing_disabled(disabled=True)

MODEL = 'gemini/gemini-2.0-flash'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

@function_tool
def add(a: int, b: int) -> int:
    print(f"Adding {a} and {b}")
    return a + b

@function_tool
def getweather(city: str) -> str:
    print(f"Fetching weather for {city}")
    return f"The weather in {city} is sunny with a high of 25°C."

def main(model:str, api_key:str):
    agent = Agent(
        name = "Assistant",
        instructions = "You are a helpful assistant.",
        model = LitellmModel(model = model, api_key = api_key),
        tools = [getweather, add],
    )

    result = Runner.run_sync(agent, "what is addition result of 2 and 3, and what is the weather in Peshawar?",)
    print(result.final_output)
main(model = MODEL, api_key = GEMINI_API_KEY)
   

