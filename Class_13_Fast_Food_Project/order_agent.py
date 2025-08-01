from dotenv import load_dotenv
from agents import Agent, function_tool, ModelSettings, RunContextWrapper
import rich
from datetime import datetime, time

#-------------------------------
load_dotenv()
#------------------------------------
def is_businnes_hours():
    now = datetime.now().time()
    business_start = time(9, 0) #9AM
    business_end = time(22, 0) #10PM
    
    return (business_start <= now) and (now <= business_end) # yahn par time check hoga phir True/False return kiyya jaega.

#------------------------------------

def close_tool_switcher(ctx: RunContextWrapper, agent: Agent)-> bool:
    """Enable shop_closed tool only when shop is closed"""
    return not is_businnes_hours() # True/False yahn par return hoga agr True aya to usy False bana diyya jaega or False ko True.


# dosri file mein is Agent k runner hai or usme context set hai to wrapper ki class yahn se hamen wo context nikal kar degi. 
def burger_tool_switcher(ctx: RunContextWrapper, agent: Agent)-> bool:
    if ctx.context.order_type == "burger":
        return True
    return False


# dosri file mein is Agent k runner hai or usme context set hai to wrapper ki class yahn se hamen wo context nikal kar degi. 
def pizza_tool_switcher(ctx: RunContextWrapper, agent: Agent)-> bool:
    if ctx.context.order_type == "pizza":
        return True
    return False

#------------------------------------

@function_tool(is_enabled=close_tool_switcher) # Yahn True aya to ye tool band ho jaega warna Khula rhega.
def shop_closed() -> str:
    """Return a standard shop close Notice"""
    
    return "Shop is closed. please comeback during business hours. (9:00AM) to (10:00PM)"

#------------------------------------

@function_tool(is_enabled=burger_tool_switcher)
def burger_order():
    """Provide an update for the status of the user`s burger order"""
    
    return "Your Burger is Cooking... please wait for just 10 minutes"

#------------------------------------
@function_tool(is_enabled=pizza_tool_switcher)
def pizza_order():
    """Provide an update for the status of the user`s pizza order"""
    
    return "Your pizza is Cooking... please wait for just 10 minutes"

#------------------------------------

my_order_agent = Agent( 
    name="my_order_agent_result",
    instructions="""always first check timing of shop by shop_closed tool if available.
                    You are a order taker manager for a fast food retuarant. 
                    always use avelible tools provided to you. 
                    if the shop_closed tool is available use it immediately. 
                    Never respond with your own text - always use a tool. """,
    model="gpt-4.1-mini",
    tools=[burger_order, pizza_order, shop_closed],
    model_settings=ModelSettings(temperature=0.3, tool_choice="required")
) 

#------------------------------------
