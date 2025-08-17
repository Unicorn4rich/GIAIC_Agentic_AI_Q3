from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled, enable_verbose_stdout_logging, trace, ModelSettings
import rich
import asyncio

#-------------------------------
load_dotenv()
# enable_verbose_stdout_logging()
# set_tracing_disabled(disabled=True)

#------------------------------------

old_settings = ModelSettings(temperature=0.7)  
new_settings = old_settings.resolve(ModelSettings(max_tokens=300, temperature=0.3)) # purani settings new settings ke sath merge karta hai or override karta hai.

#------------------------------------

agent = Agent( 
    name="my_agent",
    instructions="You are a helpful assitant",
    model="gpt-4.1-mini",
    model_settings=new_settings
) 

#------------------------------------

result1 =  Runner.run_sync(agent, input="hi") 
rich.print("Runner: ", result1)


#------------------------------------
# modelSettings

# "temp" < "0.3"
# "top-k" = "0.7" = "Select 7 words"
# "top-p" = "0.3" = "from 7 words, select only 3 most probal words"

# "am", "will", "can"
# "i am"

#------------------------------------
# First question -> Wrap trace

# async def main():
    
#     with trace("Sir Taha Workflow"):  # wrap dono Runners aik hi naam ki trace ke sath combine kar ke. 
#             result1 = await Runner.run(agent, input="hi") 
#             rich.print("Runner1: ", result1.final_output)  

#             result2 = await Runner.run(agent, input="do you know me?") 
#             rich.print("Runner2: ", result2.final_output)  



# asyncio.run(main())
