import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, ModelSettings, RunContextWrapper, function_tool
import rich
from pydantic import BaseModel


#-------------------------------
load_dotenv()
set_tracing_disabled(disabled=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#-------------------------------

class User_info(BaseModel):
    name: str
    age: int
    alive: bool
    roll_num: str
    
    
my_info = User_info(name="shoaib", age=22, alive=True, roll_num="abc1234567") 
  
#-------------------------------
# local 

def dynamic_ins(wrapper: RunContextWrapper[User_info], agent: Agent):
    wrapper.context.name = "azlaan"
    return f"when ever user ask for roll number you use given tool use shoaib_information for roll number name is {wrapper.context.name} and user age is {wrapper.context.age}"

#-------------------------------
# LLM

@function_tool # ye sync func ko bhi async bana ke chlata hai.
def shoaib_information(wrapper: RunContextWrapper[User_info], agent: Agent):
    "This function is to tell about shoaib information"
    return f"user roll number is {wrapper.context.roll_num}" # ye return first attempt mein nahi second attemp mein diyya jata hai llm ko.
    
#-------------------------------

client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

#-------------------------------

agent = Agent[User_info]( 
    name="my_agent",
    instructions=dynamic_ins,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash-lite", openai_client=client),
    tools=[shoaib_information]
)

#-------------------------------

result = Runner.run_sync(starting_agent=agent, input="what is the age of user? and what his roll number?", context=my_info) # context -> 2 option -> data LLM ko dena hai ya nahi
rich.print(result.final_output)



#-------------------------------# Notes: -------------------------------------
