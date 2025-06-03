import chainlit as cl
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)



agent = Agent(
        name="Assistant",
        instructions="You are helpful Assistent.",
        model=model
)
    

# result = Runner.run_sync(agent, "What is capital of France..", run_config=config)
# print(result.final_output)
#     # Function calls itself,
#     # Looping in smaller pieces,
#     # Endless by design.

@cl.on_message
async def handle_message(message: cl.Message):
    result = await Runner.run(agent, input = message.content, run_config=config)
    await cl.Message(content = result.final_output).send()