from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, Runner, TResponseInputItem, input_guardrail
from pydantic import BaseModel, Field


#------------------------------------
# strure validate

class Check_Slang_Class(BaseModel):
  is_abusive: bool = Field(description="Value will be True if user query has some slang or abusive language")
  reasoning: str = Field(description="what is the reason behind it")

#------------------------------------
# Guardrail agents

input_guradrail_agent = Agent( 
    name="Input Guardrail Agent",
    instructions="Always check if the user query has any abusive and slang words.",
    model="gpt-4.1-mini",
    output_type=Check_Slang_Class
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
  