from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled
import os
import rich
from agents.extensions.models.litellm_model import LitellmModel
import litellm # for warnings


load_dotenv()

litellm.disable_aiohttp_transport = True # LiteLLM ko use karte huy kuch objects data or warnings aa rhi thi jawab ke sath to ye unko htany ke liye lgaya hai.

set_tracing_disabled(disabled=True)

# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") # this is from openrouter 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # ye APi key hamen (google AI Studio) se milti hai.


# client = AsyncOpenAI(             # Not use in liteLLM
#     api_key=OPENROUTER_API_KEY,
#     base_url="https://openrouter.ai/api/v1"
# )

agent = Agent(
    name="my_agent",
    instructions="You are a helpful assistant",
    model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=GEMINI_API_KEY),
)


answer = Runner.run_sync(starting_agent=agent, input="Hi my name is shoaib")
rich.print(answer.final_output)