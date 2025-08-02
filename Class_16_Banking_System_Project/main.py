from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled, enable_verbose_stdout_logging, ModelSettings, input_guardrail, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
import rich
from my_tools import generate_customer_token, identify_banking_purpose
from output_guardrail import res_check
from input_guardrail import check_slangs
from hnadoffs_agents import account_agent, transfer_agent, loan_agent

#-------------------------------
load_dotenv()
enable_verbose_stdout_logging()
# set_tracing_disabled(disabled=True)
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