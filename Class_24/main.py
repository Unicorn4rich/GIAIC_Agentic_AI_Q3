from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled, enable_verbose_stdout_logging, trace, ModelSettings
import rich
from pydantic import BaseModel
#-------------------------------
load_dotenv()
# enable_verbose_stdout_logging()
# set_tracing_disabled(disabled=True)

#------------------------------------
# class

class MyCLass(BaseModel): # pydantic ki class ka feature ye bhi hai ke wo python ki data type ko use karta hai schema define karne mein.
    message: str

#------------------------------------

agent = Agent( 
    name="my_agent",
    instructions="You are a helpful assitant",
    model="gpt-4.1-mini",
    output_type=MyCLass
) 

#------------------------------------

result =  Runner.run_sync(agent, input="hi") 
rich.print(result.final_output.message)

#------------------------------------
# 