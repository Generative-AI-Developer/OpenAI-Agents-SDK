import os
import dotenv
dotenv.load_dotenv()
import asyncio
from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel

set_tracing_disabled(disabled=True)

MODEL = 'gemini/gemini-2.0-flash'
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if API key is loaded
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Ensure .env file is configured correctly.")

@function_tool
def get_weather(city: str) -> str:
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."

def main():  # Removed arguments
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
    )

    result = Runner.run_sync(agent, "What's the weather in Lahore?")
    print(result.final_output)

if __name__ == "__main__":
    main()  # Call main without arguments