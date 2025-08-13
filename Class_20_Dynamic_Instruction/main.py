from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled, enable_verbose_stdout_logging, RunContextWrapper, function_tool
import rich
from pydantic import BaseModel


#-------------------------------
load_dotenv()
# enable_verbose_stdout_logging()
# set_tracing_disabled(disabled=True)

#------------------------------------

class UserInfo(BaseModel):
    user_name: str


user_information = UserInfo(user_name="shoaib")


# class 
class DynClass():
    def __init__(self):
        pass
    
    def __call__(self, ctx: RunContextWrapper[UserInfo], agent: Agent):
        if ctx.context.user_name == "Basit":
            return f"Hey Basit 😌"
        elif ctx.context.user_name == "shoaib":
            return f"I am {ctx.context.user_name} 😂"    
    
    
dyn_ins = DynClass()
    

#------------------------------------
# class UserInfo(BaseModel):
#     user_name: str


# user_input = input("Enter your name: ")
# user_info_obj = UserInfo(user_name=user_input)


# dynamic instruction

# def dynamic_ins(ctx: RunContextWrapper[UserInfo], agent: Agent): # RunContextWrapper -> mein class isliye di ke user_name white par rha tha.
#     # Database
#     ctx.context.user_name = "azlaaaaan" # -> user_info_obj.user_name mein jo bhi aega wo azlaaan se replace ho jaega.
    
#     rich.print(ctx) # -> UserInfo(user_name="shoaibbbbbb") 
#     rich.print(ctx.context.user_name) # -> 
#     rich.print(agent) # -> Agent ki sari propertys jo use hoti hain wo sab dikhengi.
    
#     return f"I am {ctx.context.user_name} You are a helpful assistant"

#------------------------------------


agent = Agent( 
    name="my_agent",
    # instructions=dynamic_ins,
    instructions=dyn_ins,
    model="gpt-4.1-mini"
) 

#------------------------------------

result =  Runner.run_sync(agent, input="hi, do you know me? ", context=user_information) 
rich.print("🤓", result.final_output)

#---------------------------------------------------------------------------------------------------------------
# 