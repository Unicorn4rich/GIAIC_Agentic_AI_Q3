from agents import Agent, Runner, output_guardrail, RunContextWrapper, GuardrailFunctionOutput
from pydantic import BaseModel, Field
from typing import Any


#------------------------------------
# strure validate

class Check_Res_Class(BaseModel):
  is_not_banking_related: bool = Field(description="If the LLM response is not related to banking related topic set the value True in this field otherwise False.")
  reasoning: str = Field(description="What is the reason behind it")
  
  
#------------------------------------
# Guardrail agents

output_guradrail_agent = Agent( 
    name="Output Guardrail Agent",
    instructions="Always check if the LLM response should be only related to banking response.",
    model="gpt-4.1-mini",
    output_type=Check_Res_Class
)  


#------------------------------------
# guardrail output classes structure

@output_guardrail
async def res_check(ctx: RunContextWrapper, agent: Agent, output: Any) -> GuardrailFunctionOutput:
  
  result = await Runner.run(output_guradrail_agent, output, context=ctx)
  
  return GuardrailFunctionOutput(
    output_info=result.final_output,
    tripwire_triggered=result.final_output.is_not_banking_related
  )
  
  