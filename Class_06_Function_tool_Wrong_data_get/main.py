import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, function_tool
import rich

#-----------------------------
load_dotenv()
set_tracing_disabled(disabled=True)
OPENROUTER_API_KEY = os.getenv(('OPENROUTER_API_KEY'))
#-----------------------------
@function_tool
def karachi_weather(city: str)-> str: # is parameter mein karachi laega.
    """ 
     get the current weather of karachi.
    """
    
    return "The current weather of karachi{city} is -0C"
    
#-----------------------------

client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

agent = Agent(
    name="my_agent",
    instructions="always use karachi_weather tool when ever user ask for weather of karachi, You are a helpfull assistant",
    model=OpenAIChatCompletionsModel(model="mistralai/mistral-small-24b-instruct-2501", openai_client=client),
    tools=[karachi_weather]
)


#---------------------------------

result = Runner.run_sync(agent, "what is the weather of karachi?")
rich.print(result.final_output)