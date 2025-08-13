from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled, enable_verbose_stdout_logging, AgentHooks, RunContextWrapper, function_tool
import rich
from typing import Any

#-------------------------------
load_dotenv()
# enable_verbose_stdout_logging()
# set_tracing_disabled(disabled=True)


#------------------------------------
# Agent Hook class1

class MyAgentHook(AgentHooks):
  
     async def on_start(self, context: RunContextWrapper, agent: Agent) -> None: # Jese Agent start hoga tab ye lines chalegi.
        print("😈 My Agent starts here....")
        
     async def on_end(self, context: RunContextWrapper, agent: Agent, output: Any,) -> None: # Agent ke final_output deny ke bad ye chalta hai. 
        print("😈 My Agent ends here....")  
        
        
     async def on_handoff(self, context: RunContextWrapper, agent: Agent, source: Agent,) -> None: # handsoff se pehly chalega.
         print("🤦‍♀️ My handoffs starts here....")      


     async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool) -> None: # tools ke chalne se pehly chalega.
         print("😂 My tool starts here....")
         
     async def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool, result: str,) -> None:
         print("😂 My tool ends here....")
         
         
#------------------------------------
# Agent Hook class 2

class MySecondAgentHook(AgentHooks):
  
     async def on_start(self, context: RunContextWrapper, agent: Agent) -> None: # Jese Agent start hoga tab ye lines chalegi.
        print("😈 My Agent starts here....")
        
     async def on_end(self, context: RunContextWrapper, agent: Agent, output: Any,) -> None: # Agent ke final_output deny ke bad ye chalta hai. 
        print("😈 My Agent ends here....")  
        
        
     async def on_handoff(self, context: RunContextWrapper, agent: Agent, source: Agent,) -> None: # handsoff se pehly chalega.
         print("🤦‍♀️ My handoffs starts here....")      


     async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool) -> None: # tools ke chalne se pehly chalega.
         print("😂 My tool starts here....")
         
     async def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool, result: str,) -> None:
         print("😂 My tool ends here....")


#------------------------------------
# Tool

@function_tool
def weather_tool():
    return "Current weather is 55C"

#------------------------------------

sec_agent = Agent( 
    name="sec_agent",
    instructions="You are a helpful assistant",
    model="gpt-4.1-mini",
    # hooks=MyAgentHook(), # Aik hi Custom class dono mein pass kar sakty hain same class is agent ke chalne pe bhi work karegi.
    hooks=MySecondAgentHook(), # -> har agent ke liye alag se Custom class bana kar laga sakty hain.
) 


agent = Agent( 
    name="my_agent",
    instructions="You are a helpful assistant",
    model="gpt-4.1-mini",
    hooks=MyAgentHook(),
    handoffs=[sec_agent],
    tools=[weather_tool]
) 

#------------------------------------
# RunnerHooks or AgentHooks mein faraq ye hai ke Runner wala har aik agent ke flow pe custom bnai hui class ko laga kar chalega
# or Agent wala har aik agent pe jaaa kar lgaenge to wo agents is class ko chlaenge warna nahi
# RunnerHook or AgentHook aik sath laga kar chala den to har cheez double double aegi.

result =  Runner.run_sync(agent, input="call sec_agent, and call weather_tool") # Runner mein ham kuch bhi dety hain to instance bana kar dety hain lekin Agent mein aisa nahi hota direct dey sakty hain.
rich.print("🤓", result.final_output)




#---------------------------------------------------------------------------------------------------------------
# 