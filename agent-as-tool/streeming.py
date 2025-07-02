import os
import dotenv
dotenv.load_dotenv()
import asyncio
from agents import Agent, Runner, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from agents.extensions.visualization import draw_graph
set_tracing_disabled(disabled=True)
from openai.types.responses import ResponseTextDeltaEvent

MODEL = 'gemini/gemini-2.0-flash'
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


async def main():
    agent = Agent(
        name="AI expert",
        instructions= "You are an AI expert. You will help users with their questions and issues related to AI.",   
        model=LitellmModel(
        model=MODEL,
        api_key=GEMINI_API_KEY,
    ))

    result =  Runner.run_streamed(agent, input  = "what is streeming in openai agents sdk explain in not more than 100 words", )
# print(result.final_output)

    print(type(result),result, "\n\n")
    async for event in result.stream_events():
        print(event)

asyncio.run(main())        