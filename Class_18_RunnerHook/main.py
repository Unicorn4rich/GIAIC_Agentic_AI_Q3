from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled, enable_verbose_stdout_logging, RunHooks, RunContextWrapper, function_tool
import asyncio
import rich
from typing import Any 

#-------------------------------
load_dotenv()
enable_verbose_stdout_logging()
# set_tracing_disabled(disabled=True)

#------------------------------------
# runHook Class
class MyRunner_Hook(RunHooks):
    async def on_agent_start(self, context: RunContextWrapper, agent: Agent)-> None:
        # database logic
        # context.name = database.name -> we can update our context at run time before agent start 
        print("🤓 my agent start here.........")
        
    async def on_agent_end(self, context: RunContextWrapper, agent: Agent, output: Any,) -> None:
        print("🤓 my agent end here.........")
        
    async def on_handoff(self, context: RunContextWrapper, from_agent: Agent, to_agent: Agent) -> None:
        print("😉 my handoffs start here.........")
        

    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool) -> None:
        print("🙈 my tool starts here.........")
        

    async def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool, result: str) -> None:
        print("🙈 my tool end here.........")
        


my_runner_hook= MyRunner_Hook()

#------------------------------------
# Tool
@function_tool
def time_tool():
    return "Current time is 5:52 pm"

#------------------------------------
sec_agent = Agent( 
    name="sec_agent",
    instructions="You are a helpful assistant",
    model="gpt-4.1-mini",
) 

#------------------------------------

agent = Agent( 
    name="my_agent",
    instructions="You are a helpful assistant",
    model="gpt-4.1-mini",
    handoffs=[sec_agent],
    tools=[time_tool]
) 

#---------------------------------

result =  Runner.run_sync(agent, input="hi, call time tool and and handoffs sec_agent", hooks=my_runner_hook) 
rich.print("🙂", result.final_output)




#---------------------------------------------------------------------------------------------------------------
# RunHooks Custom class Output:


(class-17-tracing) PS D:\GOVERNER HOUSE\SIR TAHA CLASSES\GIAIC_Agentic_AI_Q3\Class_18> uv run main.py
Creating trace Agent workflow with id trace_4b3e4c15971f4fa3890ceb74ceef9f84
Setting current trace: trace_4b3e4c15971f4fa3890ceb74ceef9f84
Creating span <agents.tracing.span_data.AgentSpanData object at 0x00000134258A1C70> with id None
Running agent my_agent (turn 1)
🤓 my agent start here.........
Creating span <agents.tracing.span_data.ResponseSpanData object at 0x00000134262E5450> with id None
Calling LLM gpt-4.1-mini with input:
[
  {
    "content": "hi, call time tool and and handoffs sec_agent",
    "role": "user"
  }
]
Tools:
[
  {
    "name": "time_tool",
    "parameters": {
      "properties": {},
      "title": "time_tool_args",
      "type": "object",
      "additionalProperties": false,
      "required": []
    },
    "strict": true,
    "type": "function",
    "description": ""
  },
  {
    "name": "transfer_to_sec_agent",
    "parameters": {
      "additionalProperties": false,
      "type": "object",
      "properties": {},
      "required": []
    },
    "strict": true,
    "type": "function",
    "description": "Handoff to the sec_agent agent to handle the request. "
  }
]
Stream: False
Tool choice: NOT_GIVEN
Response format: NOT_GIVEN
Previous response id: None

LLM resp:
[
  {
    "arguments": "{}",
    "call_id": "call_OhBv8ko2alpX8qgxPJ0UMF5q",
    "name": "time_tool",
    "type": "function_call",
    "id": "fc_6895fb07423481a289c4b3188dc6b350084b37d610c2d0f3",
    "status": "completed"
  },
  {
    "arguments": "{}",
    "call_id": "call_b0sFJnH1y8ZDWboHSZd2gWGq",
    "name": "transfer_to_sec_agent",
    "type": "function_call",
    "id": "fc_6895fb07567c81a29883bfdc4c183138084b37d610c2d0f3",
    "status": "completed"
  }
]

Creating span <agents.tracing.span_data.FunctionSpanData object at 0x0000013424881220> with id None
🙈 my tool starts here.........
Invoking tool time_tool with input {}
Tool call args: [], kwargs: {}
Tool time_tool returned Current time is 5:52 pm
🙈 my tool end here.........
Creating span <agents.tracing.span_data.HandoffSpanData object at 0x00000134269482D0> with id None
😉 my handoffs start here.........
Creating span <agents.tracing.span_data.AgentSpanData object at 0x000001342487BE80> with id None
Running agent sec_agent (turn 2)
🤓 my agent start here.........
Creating span <agents.tracing.span_data.ResponseSpanData object at 0x0000013426948150> with id None
Calling LLM gpt-4.1-mini with input:
[
  {
    "content": "hi, call time tool and and handoffs sec_agent",
    "role": "user"
  },
  {
    "arguments": "{}",
    "call_id": "call_OhBv8ko2alpX8qgxPJ0UMF5q",
    "name": "time_tool",
    "type": "function_call",
    "id": "fc_6895fb07423481a289c4b3188dc6b350084b37d610c2d0f3",
    "status": "completed"
  },
  {
    "arguments": "{}",
    "call_id": "call_b0sFJnH1y8ZDWboHSZd2gWGq",
    "name": "transfer_to_sec_agent",
    "type": "function_call",
    "id": "fc_6895fb07567c81a29883bfdc4c183138084b37d610c2d0f3",
    "status": "completed"
  },
  {
    "call_id": "call_OhBv8ko2alpX8qgxPJ0UMF5q",
    "output": "Current time is 5:52 pm",
    "type": "function_call_output"
  },
  {
    "call_id": "call_b0sFJnH1y8ZDWboHSZd2gWGq",
    "output": "{\"assistant\": \"sec_agent\"}",
    "type": "function_call_output"
  }
]
Tools:
[]
Stream: False
Tool choice: NOT_GIVEN
Response format: NOT_GIVEN
Previous response id: None

Exported 1 items
LLM resp:
[
  {
    "id": "msg_6895fb0902bc81a28139dd2467a2109a084b37d610c2d0f3",
    "content": [
      {
        "annotations": [],
        "text": "The current time is 5:52 PM. I am transferring the conversation to the security agent now.",
        "type": "output_text",
        "logprobs": []
      }
    ],
    "role": "assistant",
    "status": "completed",
    "type": "message"
  }
]

🤓 my agent end here.........
Resetting current trace
🙂 The current time is 5:52 PM. I am transferring the conversation to the security agent now.
Shutting down trace provider
Shutting down trace processor <agents.tracing.processors.BatchTraceProcessor object at 0x000001342475A900>
Exported 4 items
Exported 2 items
(class-17-tracing) PS D:\GOVERNER HOUSE\SIR TAHA CLASSES\GIAIC_Agentic_AI_Q3\Class_18> 