from dotenv import load_dotenv
from agents import Agent, Runner, ModelSettings, enable_verbose_stdout_logging, Handoff, RunContextWrapper
from pydantic import BaseModel
import rich
from agents.extensions import handoff_filters

#-------------------------------
load_dotenv()
enable_verbose_stdout_logging()
#-------------------------------


billing_agent = Agent( 
    name="billing_agent",
    instructions="you handle all billing-related queries, provide clear and concise information rearding billing billing.",
    handoff_description="you support user in billing issues.",
    model="gpt-4.1-mini",
)  
  
#-------------------------------
refund_agent = Agent( 
    name="refund_agent",
    instructions="you handle all refund-related queries, assist users in processing refunds efficiently.",
    model="gpt-4.1-mini",
)  
  
#-------------------------------
class Model_refund(BaseModel):
    input: str
    
my_schema = Model_refund().model_json_schema()
my_schema["additionalProperties"] = False
#-------------------------------

async def my_invoke_function(ctx: RunContextWrapper, input:str,):
        
    rich.print("input", input)    
    return refund_agent

#-------------------------------
def my_enable(ctx: RunContextWrapper, agent: Agent):
    return True

#-------------------------------
refund_agent_handoff = Handoff(
    agent_name="refund_agent",
    tool_name = "refund_agent",
    tool_description="You provide support to user on refund process.",
    input_json_schema=my_schema,
    on_invoke_handoff=my_invoke_function,
    input_filter=handoff_filters.remove_all_tools,
    strict_jason_schema=True, # Ye structre output follow krata hai true pe.
    is_enabled=True # On/Off
)

#-------------------------------
triage_agent = Agent( 
    name="triage_agent",
    instructions="you always delegate task to appropriate agent.",
    model="gpt-4.1-mini",
    tools=[billing_agent, refund_agent_handoff],
    
)  
  
#-------------------------------
result = Runner.run_sync(triage_agent, input="hi, i have some billin iussues, please call billing_agent", max_turn=2) 
print(result.final_output) 
print("🤖", result._last_agent.name) 



#-------------------------------------------------------------------------------------------------------------------
# Notes:

# User Prompt     -> User input
# System Prompt   -> User input
# tools           -> function / handoffs_agent
# tool message    -> function return  