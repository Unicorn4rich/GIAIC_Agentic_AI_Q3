from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled, enable_verbose_stdout_logging, function_tool, ModelSettings, input_guardrail, TResponseInputItem, output_guardrail, RunContextWrapper, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
import rich
from pydantic import BaseModel, Field
from typing import Any
import random
from typing import Literal


#-------------------------------
load_dotenv()
enable_verbose_stdout_logging()
# set_tracing_disabled(disabled=True)
#------------------------------------

#------------------------------------
# strure validate

class Check_Slang_Class(BaseModel):
  is_abusive: bool = Field(description="Value will be True if user query has some slang or abusive language")
  reasoning: str = Field(description="what is the reason behind it")

class Check_Res_Class(BaseModel):
  is_not_banking_related: bool = Field(description="If the LLM response is not related to banking related topic set the value True in this field otherwise False.")
  reasoning: str = Field(description="What is the reason behind it")

#------------------------------------
# Guardrail agents

input_guradrail_agent = Agent( 
    name="Input Guardrail Agent",
    instructions="Always check if the user query has any abusive and slang words.",
    model="gpt-4.1-mini",
    output_type=Check_Slang_Class
)  


output_guradrail_agent = Agent( 
    name="Output Guardrail Agent",
    instructions="Always check if the LLM response should be only related to banking response.",
    model="gpt-4.1-mini",
    output_type=Check_Res_Class
)  


#------------------------------------
# guardrail output classes structure

@input_guardrail
async def check_slangs(ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem])-> GuardrailFunctionOutput:
  
  result = await Runner.run(input_guradrail_agent, input, context=ctx )
  
  return GuardrailFunctionOutput(
    output_info= result.final_output,
    tripwire_triggered= result.final_output.is_abusive
  )
  
  

@output_guardrail
async def res_check(ctx: RunContextWrapper, agent: Agent, output: Any) -> GuardrailFunctionOutput:
  
  result = await Runner.run(output_guradrail_agent, output, context=ctx)
  
  return GuardrailFunctionOutput(
    output_info=result.final_output,
    tripwire_triggered=result.final_output.is_not_banking_related
  )
  

#------------------------------------
# pydantic classes

class ServiceType(BaseModel):
  service: str
  confidance: float
  # keywords_detected: list[Literal["balance", "account", "statement"]] = ["account", "balance", "statement"]
  keywords_detected: list[str]
  reasoning: str


# Structure define class.
class Toolinfo(BaseModel): # is class mein values LLM nahi balke ham manuly daal rhy hain Fields llm ke liye hoti hain.
  token_number: str = Field(..., description="This takes token number.")
  wait_time: str = Field(..., description="This takes wait time value.")
  message: str = Field(..., description="This takes message.")
  service_type: str = Field(..., description="This takes service_type value.")

#------------------------------------
# tools

# 1
@function_tool
def identify_banking_purpose(customer_request: str):
  """It is a simple function to figure out what banking service customer need."""
  
  request = customer_request.lower()
  
  if ("balance" in request) or ("account" in request) or ("statement" in request):
    return ServiceType( # instance of class or isme ham keyword argument mein values dey rhy hain ot return kar rhy hain function ko.
      service= "account_service",
      confidance= 0.9,
      keywords_detected= ["balance", "account", "statement"],
      reasoning= "Customer want to check their account",
    )
    
  elif ("transfer" in request) or ("send" in request) or ("payment" in request):
    return ServiceType(
      service= "transfer_service",
      confidance= 0.9,
      keywords_detected= ["balance", "send" "payment"],
      reasoning= "Customer want to send money or make payment"
    )
    
  elif ("loan" in request) or ("mortgage" in request) or ("borrow" in request):
    return ServiceType(
      service= "loan_service",
      confidance= 0.9,
      keywords_detected= ["loan", "mortgage" "borrow"],
      reasoning= "Customer need help with loan."
    )
    
  else:
    return ServiceType(
      service= "general_banking",
      confidance= 0.5,
      keywords_detected= ["general"],
      reasoning= "Customer needs general banking help."
    )    
      


#------------------------------------
# 2

@function_tool
def generate_customer_token(service_type: Literal["general", "account_service", "transfer_service", "loan_service"])-> Toolinfo:
  """Generate a token number for the customer queue. The value of the service_type argument can be only these as mention below.
  
     service_type Args here:
     service_type = general
     service_type = account_service
     service_type = transfer_service
     service_type = loan_service
  """ 
  
  if service_type == "account_service":
    prefix = "A"
    wait_time = "5-10 minutes"
  elif service_type == "transfer_service":
    prefix = "T"
    wait_time = "2-5 minutes"
  elif service_type == "loan_service":
    prefix = "L"
    wait_time = "15-20 minutes"
  else:
    prefix = "G"
    wait_time = "8-10 minutes"  
  
  token_number = f"{prefix}-{random.randint(100, 999)}"
  
  return Toolinfo(
    token_number= token_number,
    wait_time= wait_time,
    message= f"Please take token {token_number}. and wait for a {wait_time} and have a seat, we will call you shortly.",
    service_type= service_type
  )
  
  
#------------------------------------
# specialist agents

account_agent = Agent( 
    name="Account Services Agent",
    instructions="You help user in their query of account balance, statement, and account information, always create a token!. ",
    model="gpt-4.1-mini",
    output_guardrails=[res_check]
) 

transfer_agent = Agent( 
    name="Transfer Services Agent",
    instructions="You help user with money transfer and payments, always create a token!. ",
    model="gpt-4.1-mini",
    output_guardrails=[res_check]
) 

loan_agent = Agent( 
    name="Loan Services Agent",
    # instructions="You help user with loans and mortgages, always create a token!. ",
    instructions="never reply according to banking . ",
    model="gpt-4.1-mini",
    output_guardrails=[res_check]
) 


#------------------------------------
# main agent
# instructions ko hamne Markdown or Chain of thought mein likha hai.

agent = Agent( 
    name="Bank Greeting Agent",
    instructions="""
    You are a friendly bank greeting agent.
    
    1. welcome customer nicely.
    2. use identify_banking_purpose to understand user need.
    3. if confidence > 0.8, send user to the right speciallist.
    4. always use generate_customer_token tool to generate token for the customer.
    
    # Example: argument for the generate_customer_token can only be:(
     service_type Args here: service_type = general, or service_type = account_service, or service_type = transfer_service, or service_type = loan_service      
    )
    
    5. if user is asking about other then account, transfer and loan so it is a general question. always create a token.
    
    always be helpful
    """,
    model="gpt-4.1-mini",
    tool_use_behavior="run_llm_again",
    model_settings=ModelSettings(tool_choice="auto"),
    handoffs=[account_agent, transfer_agent, loan_agent],
    tools=[generate_customer_token, identify_banking_purpose],
    input_guardrails=[check_slangs],
    output_guardrails=[res_check]
) 

#---------------------------------

while True:
  try:
    user_input = input("\n🤖 Enter your query: ")
    if user_input.lower() in ['quit', 'exit', 'back']: break
  
    result =  Runner.run_sync(agent, input=user_input) 
    rich.print("✌", result.final_output)
    print("😘", result._last_agent.name )
  except InputGuardrailTripwireTriggered as e:
    print("❌ Please Enter Bank related questions or query: ", e)   
  except OutputGuardrailTripwireTriggered as e:
    print("❌ Somthing went wrong: ", e)   