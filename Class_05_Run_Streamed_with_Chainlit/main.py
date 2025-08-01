import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled
import rich
import chainlit as cl

#-----------------------------
load_dotenv()
set_tracing_disabled(disabled=True)
OPENROUTER_API_KEY = os.getenv(('OPENROUTER_API_KEY'))
#-----------------------------
history = []
#-----------------------------

client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

agent = Agent(
    name="my_agent",
    instructions="You are a helpfull assistant",
    model=OpenAIChatCompletionsModel(model="deepseek/deepseek-r1-0528:free", openai_client=client)
)

#-----------------------------

@cl.on_message
async def my_message(msg: cl.Message):
    user_input = msg.content
    history.append({"role": "user", "content": user_input})
    message = cl.Message(content="")
    
    result = Runner.run_streamed(agent, history)
    # rich.print(result.final_output)
    
    async for event in result.stream_events():
        if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
            await message.stream_token(event.data.delta) 
