import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig
import rich


#-----------------------
load_dotenv()

GEMINI_APY_KEY = os.getenv("GEMINI_APY_KEY")

#-----------------------

agent = Agent(
    name="my_agent",
    instructions="you are a helpful assistant",
)

#-----------------------

client = AsyncOpenAI(
    api_key=GEMINI_APY_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

config = RunConfig(
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    model_provider=client,
    tracing_disabled=True
)

result = Runner.run_sync(agent, "hi", run_config=config )
rich.print(result.final_output)


# Run Level => isme ham Runner mein configrations karty hain taky runner jitne bhi agents chlaye ye sab pe apply hon.