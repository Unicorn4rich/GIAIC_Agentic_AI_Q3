from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled, input_guardrail, GuardrailFunctionOutput, RunContextWrapper, TResponseInputItem, InputGuardrailTripwireTriggered, enable_verbose_stdout_logging
import rich
from pydantic import BaseModel, Field

#-------------------------------
load_dotenv()
enable_verbose_stdout_logging()
set_tracing_disabled(disabled=True)
#------------------------------------

class Prime_Minister_Check(BaseModel):
    is_prime_minister: bool = Field(description="If user is asking anything about prime minister insert the True in this Field Otherwise insert False")
    
#------------------------------------

second_agent = Agent(
    name="second_agent",
    instructions="if user asking about president, so additionlly tell about prim minister and reply to user",
    model="gpt-4.1-mini",
    output_type=Prime_Minister_Check,
    handoff_description="You tell user about president and prime minister"
)

#------------------------------------

guardrail_agent = Agent(
    name="guardrail_agent",
    instructions="You check if the user asking about prime minister or not",
    model="gpt-4.1-mini",
    output_type=Prime_Minister_Check,
    handoffs=[second_agent]
)

#------------------------------------

@input_guardrail                                              # TResponseInputItem -> {"role": "user", "content": "hi"}
async def prime_minister_check(ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    
    guardrail_result = await Runner.run(guardrail_agent, input, context=ctx)
    
    return GuardrailFunctionOutput(
        output_info=guardrail_result.final_output,
        tripwire_triggered=guardrail_result.final_output.is_prime_minister,
        
    )

#------------------------------------

triag_agent = Agent( 
    name="triag_agent",
    instructions="You are a helpful assistant",
    model="gpt-4.1-mini",
    input_guardrails=[prime_minister_check]
) 
#---------------------------------

try:
    result =  Runner.run_sync(triag_agent, input="hi, tell who is the prime minister of pkistan, call second agent") 
    rich.print("✌", result.final_output) 

except InputGuardrailTripwireTriggered as e:
    print("❌", f"Prime minister ke bare mein baat nahi karo bhai warna: ({e}) ho jaega.")
    
    
    
#----------------------------------------------------------------------------------------------------------------    
# Verbose Workflow


PS D:\GOVERNER HOUSE\SIR TAHA CLASSES\GIAIC_Agentic_AI_Q3_Classes\Class_14> uv run main.py
Tracing is disabled. Not creating trace Agent workflow
Setting current trace: no-op
Tracing is disabled. Not creating span <agents.tracing.span_data.AgentSpanData object at 0x000001BDC5CDF7F0>    
Running agent triag_agent (turn 1)
Tracing is disabled. Not creating span <agents.tracing.span_data.GuardrailSpanData object at 0x000001BDC5CE1450>
Tracing is disabled. Not creating span <agents.tracing.span_data.AgentSpanData object at 0x000001BDC5D09D60>    
Running agent guardrail_agent (turn 1)
Tracing is disabled. Not creating span <agents.tracing.span_data.ResponseSpanData object at 0x000001BDC5CE0750>
Calling LLM gpt-4.1-mini with input:
[
  {
    "content": "hi, tell who is the prime minister of pkistan, call second agent",
    "role": "user"
  }
]
Tools:
[]
Stream: False
Tool choice: NOT_GIVEN
Response format: NOT_GIVEN
Previous response id: None

Tracing is disabled. Not creating span <agents.tracing.span_data.ResponseSpanData object at 0x000001BDC5CE32D0>
Calling LLM gpt-4.1-mini with input:
[
  {
    "content": "hi, tell who is the prime minister of pkistan, call second agent",
    "role": "user"
  }
]
Tools:
[
  {
    "name": "transfer_to_second_agent",
    "parameters": {
      "additionalProperties": false,
      "type": "object",
      "properties": {},
      "required": []
    },
    "strict": true,
    "type": "function",
    "description": "Handoff to the second_agent agent to handle the request. You tell user about president and prime minister"
  }
]
Stream: False
Tool choice: NOT_GIVEN
Response format: {'format': {'type': 'json_schema', 'name': 'final_output', 'schema': {'properties': {'is_prime_minister': {'description': 'If user is asking 
anything about prime minister insert the True in this Field Otherwise insert False', 'title': 'Is Prime Minister', 'type': 'boolean'}}, 'required': ['is_prime_minister'], 'title': 'Prime_Minister_Check', 'type': 'object', 'additionalProperties': False}, 'strict': True}}
Previous response id: None

LLM resp:
[
  {
    "arguments": "{}",
    "call_id": "call_ERYFekna90cYcHufpQGaXYDr",
    "name": "transfer_to_second_agent",
    "type": "function_call",
    "id": "fc_68823d7670208199927b9b17f924459d0cb35302c2151e2f",
    "status": "completed"
  }
]

Tracing is disabled. Not creating span <agents.tracing.span_data.HandoffSpanData object at 0x000001BDC5B3C910>
Tracing is disabled. Not creating span <agents.tracing.span_data.AgentSpanData object at 0x000001BDC6267DE0>
Running agent second_agent (turn 2)
Tracing is disabled. Not creating span <agents.tracing.span_data.ResponseSpanData object at 0x000001BDC638BD90>
Calling LLM gpt-4.1-mini with input:
[
  {
    "content": "hi, tell who is the prime minister of pkistan, call second agent",
    "role": "user"
  },
  {
    "arguments": "{}",
    "call_id": "call_ERYFekna90cYcHufpQGaXYDr",
    "name": "transfer_to_second_agent",
    "type": "function_call",
    "id": "fc_68823d7670208199927b9b17f924459d0cb35302c2151e2f",
    "status": "completed"
  },
  {
    "call_id": "call_ERYFekna90cYcHufpQGaXYDr",
    "output": "{\"assistant\": \"second_agent\"}",
    "type": "function_call_output"
  }
]
Tools:
[]
Stream: False
Tool choice: NOT_GIVEN
Response format: {'format': {'type': 'json_schema', 'name': 'final_output', 'schema': {'properties': {'is_prime_minister': {'description': 'If user is asking 
anything about prime minister insert the True in this Field Otherwise insert False', 'title': 'Is Prime Minister', 'type': 'boolean'}}, 'required': ['is_prime_minister'], 'title': 'Prime_Minister_Check', 'type': 'object', 'additionalProperties': False}, 'strict': True}}
Previous response id: None

LLM resp:
[
  {
    "id": "msg_68823d76419c8198aecc1e926e80392b05938f13cada52e1",
    "content": [
      {
        "annotations": [],
        "text": "The current Prime Minister of Pakistan is Anwaar-ul-Haq Kakar (as of 2024). \n\nI am now calling the second agent for any additional details 
or confirmation. Please hold on.",
        "type": "output_text",
        "logprobs": []
      }
    ],
    "role": "assistant",
    "status": "completed",
    "type": "message"
  }
]

LLM resp:
[
  {
    "id": "msg_68823d782cd481999f36b3d03a8c89230cb35302c2151e2f",
    "content": [
      {
        "annotations": [],
        "text": "{\"is_prime_minister\":true}",
        "type": "output_text",
        "logprobs": []
      }
    ],
    "role": "assistant",
    "status": "completed",
    "type": "message"
  }
]

Resetting current trace
❌ Prime minister ke bare mein baat nahi karo bhai warna: (Guardrail InputGuardrail triggered tripwire) ho jaega.
PS D:\GOVERNER HOUSE\SIR TAHA CLASSES\GIAIC_Agentic_AI_Q3_Classes\Class_14> 