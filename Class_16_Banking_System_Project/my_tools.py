import random
from typing import Literal
from agents import function_tool
from pydantic import BaseModel, Field


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
  