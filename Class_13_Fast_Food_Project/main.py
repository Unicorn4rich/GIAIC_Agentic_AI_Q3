from dotenv import load_dotenv
from agents import Agent, Runner, enable_verbose_stdout_logging, set_tracing_disabled
import rich
from pydantic import BaseModel, Field
from typing import Literal
from order_agent import my_order_agent

#-------------------------------
load_dotenv()
# enable_verbose_stdout_logging()
set_tracing_disabled(disabled=True)
#------------------------------------

class Order_Checker(BaseModel):
    is_order: bool = Field(
        description="Set to True if the user is placing an order specifically for pizza or burger; otherwise, False."
    )
    
    quantity: int = Field(
        default=0, description="Specify the number of items (pizza or burger) ordered by the user."
    )
    
    order_type: Literal["pizza", "burger", None] = Field(
        description="Set to 'pizza' or 'burger' according to the user's order; set to None if the request is unrelated or not food-related."
    )
    
    reason: str = Field(
        description="Provide a concise summary explaining why the request is unrelated to pizza/burger or a summary of the user’s question/request if it is non-order related."
    )
    
    user_question: str = Field(
        description="Exact text of the user's original question or request."
    )
    
#------------------------------------

main_agent = Agent( 
    name="main_agent",
    instructions="You are a knowledgeable and helpful assistant for a fast food restaurant that handles queries strictly related to pizza and burger orders. When the user is placing an order or asks questions about pizza or burgers, provide accurate and relevant assistance. For any other requests or questions unrelated to pizza or burgers, respond by summarizing the user’s intent appropriately without assuming it relates to food.",
    model="gpt-4.1-mini",
    output_type=Order_Checker
) 
#---------------------------------

user_input = input("Enter you Order: ")

result =  Runner.run_sync(main_agent, input=user_input) 
rich.print("✌", result.final_output) 
# rich.print(result.to_input_list()) # Agent + LLM conversation in list of objects

if result.final_output.is_order == True:
    my_order_agent_result = Runner.run_sync(my_order_agent, input=result.to_input_list(), context=result.final_output) # Coversation history between agent and ullm
    rich.print("😂", my_order_agent_result.final_output)





#---------------------------------

# improve my instruction and description according to gpt 4.1 prompting guide 
# "link gpt4.1 documentation"

# do not change any code

# code
# """

# """