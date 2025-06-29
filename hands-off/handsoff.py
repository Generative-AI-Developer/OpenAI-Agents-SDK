import os
import dotenv
dotenv.load_dotenv()
import asyncio
from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from agents import enable_verbose_stdout_logging

set_tracing_disabled(disabled=True)
enable_verbose_stdout_logging()

MODEL = 'gemini/gemini-2.0-flash'
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


@function_tool
def get_weather(city: str) -> str:
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."



urdu_agent = Agent(
    name="mathematical agent",
    instructions="You only respond of math related questions.",
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
)

english_agent = Agent(
    name="English agent",
    instructions="You only respond to English questions.",
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),

)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on subject request.",
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
    handoffs=[urdu_agent, english_agent],
    tools=[get_weather],
)


async def main(input: str):
    result = await Runner.run(triage_agent, input=input)
    print(result.final_output)
    print(result.last_agent.name)
asyncio.run(main("what is weather is Peshawar"))

