from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled, enable_verbose_stdout_logging, output_guardrail, RunContextWrapper, GuardrailFunctionOutput, OutputGuardrailTripwireTriggered, trace
import rich
from pydantic import BaseModel, Field
from typing import Any

#-------------------------------
load_dotenv()
enable_verbose_stdout_logging()
set_tracing_disabled(disabled=True)
#------------------------------------

class President_Check_Class(BaseModel):
  is_president: bool = Field(description="insert True if the user is asking about President, otherwise False.")
  

#------------------------------------

guardraild_aegnt = Agent( # output guardrail paralely nahi chal pata.
  name="guardraild_aegnt",
  instructions="always check if user is asking about president or not.",
  model="gpt-4.1-mini",
  output_type=President_Check_Class
)

#------------------------------------

@output_guardrail # output ki class ko function se cheezen nikal kar dey rha hota hai.
async def president_check(ctx: RunContextWrapper, agent: Agent,  output: Any) -> GuardrailFunctionOutput:
  
  guardrail_result = await Runner.run(guardraild_aegnt, output, context=ctx)
  
  return GuardrailFunctionOutput(
    output_info=guardrail_result.final_output,
    tripwire_triggered=guardrail_result.final_output.is_president
  )


#------------------------------------
sec_agent = Agent(
    name="sec_agent",
    instructions="If the user is asking about president also tell him additionally about the prime minister.",
    model="gpt-4.1-mini",
    output_guardrails=[president_check]
)
#------------------------------------

triag_agent = Agent( 
    name="triag_agent",
    instructions="You are a helpful assistant",
    model="gpt-4.1-mini",
    output_guardrails=[president_check],
    handoffs=[sec_agent]
) 
#---------------------------------


try:
  with trace("Shoaib Workflow"): # name change -> Agent workflow -> to -> Shoaib Workflow
    result =  Runner.run_sync(triag_agent, input="who was the president of pakistan in 2023, delegate to sec_agent") 
    rich.print("✌", result.final_output) 
except OutputGuardrailTripwireTriggered as e:
  rich.print("❌", e)

    
    
#----------------------------------------------------------------------------------------------------------------    
# Verbose flow with output guardrail True:


# (class-26-output-guardrail) PS D:\GOVERNER HOUSE\SIR TAHA CLASSES\GIAIC_Agentic_AI_Q3_Classes\Class_16> uv run main.py
# Tracing is disabled. Not creating trace Agent workflow
# Setting current trace: no-op
# Tracing is disabled. Not creating span <agents.tracing.span_data.AgentSpanData object at 0x000002BE0EF38050>
# Running agent triag_agent (turn 1)
# Tracing is disabled. Not creating span <agents.tracing.span_data.ResponseSpanData object at 0x000002BE0D525690>
# Calling LLM gpt-4.1-mini with input:
# [
#   {
#     "content": "who was the president of pakistan in 2023, delegate to sec_agent",
#     "role": "user"
#   }
# ]
# Tools:
# [
#   {
#     "name": "transfer_to_sec_agent",
#     "parameters": {
#       "additionalProperties": false,
#       "type": "object",
#       "properties": {},
#       "required": []
#     },
#     "strict": true,
#     "type": "function",
#     "description": "Handoff to the sec_agent agent to handle the request. "       
#   }
# ]
# Stream: False
# Tool choice: NOT_GIVEN
# Response format: NOT_GIVEN
# Previous response id: None

# LLM resp:
# [
#   {
#     "arguments": "{}",
#     "call_id": "call_LU7tasd89z8Oj0iB5wjnQQKs",
#     "name": "transfer_to_sec_agent",
#     "type": "function_call",
#     "id": "fc_68877ba902e88199973fe16b0bda52b0045489d626e660d6",
#     "status": "completed"
#   }
# ]

# Tracing is disabled. Not creating span <agents.tracing.span_data.HandoffSpanData object at 0x000002BE0EED4990>
# Tracing is disabled. Not creating span <agents.tracing.span_data.AgentSpanData object at 0x000002BE0F4A1EF0>
# Running agent sec_agent (turn 2)
# Tracing is disabled. Not creating span <agents.tracing.span_data.ResponseSpanData object at 0x000002BE0E661DD0>
# Calling LLM gpt-4.1-mini with input:
# [
#   {
#     "content": "who was the president of pakistan in 2023, delegate to sec_agent",
#     "role": "user"
#   },
#   {
#     "arguments": "{}",
#     "call_id": "call_LU7tasd89z8Oj0iB5wjnQQKs",
#     "name": "transfer_to_sec_agent",
#     "type": "function_call",
#     "id": "fc_68877ba902e88199973fe16b0bda52b0045489d626e660d6",
#     "status": "completed"
#   },
#   {
#     "call_id": "call_LU7tasd89z8Oj0iB5wjnQQKs",
#     "output": "{\"assistant\": \"sec_agent\"}",
#     "type": "function_call_output"
#   }
# ]
# Tools:
# []
# Stream: False
# Tool choice: NOT_GIVEN
# Response format: NOT_GIVEN
# Previous response id: None

# LLM resp:
# [
#   {
#     "id": "msg_68877ba9eb648199b3e4058c20bf78a2045489d626e660d6",
#     "content": [
#       {
#         "annotations": [],
#         "text": "In 2023, the President of Pakistan was Arif Alvi. Additionally, the Prime Minister of Pakistan in 2023 was Shehbaz Sharif. If you need more detailed information about their terms or roles, feel free to ask!",
#         "type": "output_text",
#         "logprobs": []
#       }
#     ],
#     "role": "assistant",
#     "status": "completed",
#     "type": "message"
#   }
# ]

# Tracing is disabled. Not creating span <agents.tracing.span_data.GuardrailSpanData object at 0x000002BE0EF1F410>
# Tracing is disabled. Not creating span <agents.tracing.span_data.AgentSpanData object at 0x000002BE0F4A3980>
# Running agent guardraild_aegnt (turn 1)
# Tracing is disabled. Not creating span <agents.tracing.span_data.ResponseSpanData object at 0x000002BE0F52FA10>
# Calling LLM gpt-4.1-mini with input:
# [
#   {
#     "content": "In 2023, the President of Pakistan was Arif Alvi. Additionally, the Prime Minister of Pakistan in 2023 was Shehbaz Sharif. If you need more detailed information about their terms or roles, feel free to ask!",
#     "role": "user"
#   }
# ]
# Tools:
# []
# Stream: False
# Tool choice: NOT_GIVEN
# Response format: {'format': {'type': 'json_schema', 'name': 'final_output', 'schema': {'properties': {'is_president': {'description': 'insert True if the user 
# is asking about President, otherwise False.', 'title': 'Is President', 'type': 'boolean'}}, 'required': ['is_president'], 'title': 'President_Check_Class', 'type': 'object', 'additionalProperties': False}, 'strict': True}}
# Previous response id: None

# LLM resp:
# [
#   {
#     "id": "msg_68877bad48c4819bb4637c21d908b1e201bc9ec1ab6f4c55",
#     "content": [
#       {
#         "annotations": [],
#         "text": "{\"is_president\":true}",
#         "type": "output_text",
#         "logprobs": []
#       }
#     ],
#     "role": "assistant",
#     "status": "completed",
#     "type": "message"
#   }
# ]

# Resetting current trace
# ❌ Guardrail OutputGuardrail triggered tripwire
# (class-26-output-guardrail) PS D:\GOVERNER HOUSE\SIR TAHA CLASSES\GIAIC_Agentic_AI_Q3_Classes\Class_16>





























