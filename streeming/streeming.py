import os
import dotenv
dotenv.load_dotenv()
import asyncio
import random
from agents import Agent, function_tool, Runner, set_tracing_disabled, ItemHelpers
from agents.extensions.models.litellm_model import LitellmModel
from agents.extensions.visualization import draw_graph
set_tracing_disabled(disabled=True)
from openai.types.responses import ResponseTextDeltaEvent


MODEL = 'gemini/gemini-2.0-flash'
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


@function_tool
def how_many_jokes() -> int:
    return random.randint(1, 10)


async def main():
    agent = Agent(
        name="Joker",
        instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
        tools=[how_many_jokes],
        model=LitellmModel(
        model=MODEL,
        api_key=GEMINI_API_KEY,
    ))

    result = Runner.run_streamed(
        agent,
        input="Hello",
    )
    print("=== Run starting ===")

    async for event in result.stream_events():
        # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            continue
        # When the agent updates, print that
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        # When items are generated, print them
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass  # Ignore other event types

    print("=== Run complete ===")


if __name__ == "__main__":
    asyncio.run(main())