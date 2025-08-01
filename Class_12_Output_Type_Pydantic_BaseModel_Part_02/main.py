from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, ModelSettings, enable_verbose_stdout_logging
import rich
from pydantic import BaseModel, Field
from typing import Literal


#-------------------------------
load_dotenv()
# enable_verbose_stdout_logging()
#------------------------------------

class Order_check(BaseModel):
    is_order: bool = Field(description="if user has some order of pizza, insert the value of True in this field")
    quantity: int = Field(description="Write the quantity of user order")
    order_type: Literal["Pizza", "Burger", None] = Field(description="If user has order not related to my literal value of pizza and burger keep the value of this field as None")
    
#---------------------------------

@function_tool(is_enabled=True)
def order_completion(order: Order_check) -> str:
    """This tool helps users to tell your order is ready"""
    return (f"Your order of {order.quantity} {order.order_type} is ready, Enjoy your meal")
    
    
@function_tool(is_enabled=True)
def order_waiting(order: Order_check) -> str:
    """This tool tells user of status of his order"""
    return (f"Your order of {order.quantity} {order.order_type}  will be ready in 10 minutes, Tank you for your patience")
    
#------------------------------

triage_agent = Agent( 
    name="triage_agent",
    instructions="always use tool order_waiting and order_completion if user has any order related to pizza and burger.",
    model="gpt-4.1-mini",
    output_type=Order_check,
    tools=[order_waiting, order_completion],
    model_settings=ModelSettings(tool_choice="required") # lazim ye wala tool use karea.
) 
 
#---------------------------------

result =  Runner.run_sync(triage_agent, input="hi i am shoaib i want pizza 1 large and 1 reguler") 
rich.print("😈", result.final_output) # Order_check(is_order=True, quantity=2, order_type='Pizza')





