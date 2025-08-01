import os
from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled, det_default_openai_api, set_default_openai_client, AsyncOpenAI
import rich


#------------------------------------
# Global mein ham jitne Agents create karegne wo sab Gemini pe chalenge dosry kisi llm pe nahi kiyun ke sari setting iski hui huwi hai.

load_dotenv()
set_tracing_disabled(disabled=True)
det_default_openai_api("chat_completions")
GEMINI_APY_KEY = os.getenv("GEMINI_APY_KEY")
#------------------------------------

client = AsyncOpenAI(
    api_key=GEMINI_APY_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

set_default_openai_client(client)
#------------------------------------

agent = Agent(
    name="my_agent",
    instructions="you are a helpful assistant",
    model="gemini-2.0-flash"
)

#------------------------------------
result = Runner.run_sync(agent, "hi")
rich.print(result.final_output)

















# Global level mein ham configration na to Agent mrin karty hain or naa Runner mein.