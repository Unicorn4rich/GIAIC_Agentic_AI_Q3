triage agent se handsoff ka flow =>

PS D:\GOVERNER HOUSE\SIR TAHA CLASSES\PIAIC_AGENTIC_AI_CLasses_Q2\Class_19_handoff_details_Code_2> uv run app.py
Creating trace Agent workflow with id trace_71dc287cabf64f08acfce7e966ddca59
Setting current trace: trace_71dc287cabf64f08acfce7e966ddca59
Creating span <agents.tracing.span_data.AgentSpanData object at 0x000001D3985E19A0> with id None
Running agent triage_agent (turn 1)
Creating span <agents.tracing.span_data.ResponseSpanData object at 0x000001D3985B4510> with id None
Calling LLM gpt-4.1-mini with input:
[
  {
    "content": "i am shoaib, call customer_support_filter tool",
    "role": "user"
  }
]
Tools:
[
  {
    "name": "greeting",
    "parameters": {
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        }
      },
      "required": [
        "name"
      ],
      "title": "greeting_args",
      "type": "object",
      "additionalProperties": false
    },
    "strict": true,
    "type": "function",
    "description": ""
  },
  {
    "name": "customer_support_filter",
    "parameters": {
      "additionalProperties": false,
      "type": "object",
      "properties": {},
      "required": []
    },
    "strict": true,
    "type": "function",
    "description": "Handoff to the customer_support agent to handle the request. "
  },
  {
    "name": "customer_support_no_filter",
    "parameters": {
      "additionalProperties": false,
      "type": "object",
      "properties": {},
      "required": []
    },
    "strict": true,
    "type": "function",
    "description": "Handoff to the customer_support agent to handle the request. "
  }
]
Stream: False
Tool choice: NOT_GIVEN
Response format: NOT_GIVEN
Previous response id: None

LLM resp:
[
  {
    "arguments": "{\"name\":\"shoaib\"}",
    "call_id": "call_hDEfh4wazwmI4y2BzDbibCRD",
    "name": "greeting",
    "type": "function_call",
    "id": "fc_686be9b19958819a92d285de7514a130008ac72609844608",
    "status": "completed"
  },
  {
    "arguments": "{}",
    "call_id": "call_yfdhjrmqQxvQbNm50nXNNqFI",
    "name": "customer_support_filter",
    "type": "function_call",
    "id": "fc_686be9b1ef40819a939f918120f3bfd0008ac72609844608",
    "status": "completed"
  }
]

Creating span <agents.tracing.span_data.FunctionSpanData object at 0x000001D398B3F930> with id None
Invoking tool greeting with input {"name":"shoaib"}
Tool call args: ['shoaib'], kwargs: {}
Tool greeting returned hello nice to meet you shoaib
Creating span <agents.tracing.span_data.HandoffSpanData object at 0x000001D398B2BF90> with id None
Filtering inputs for handoff
Creating span <agents.tracing.span_data.AgentSpanData object at 0x000001D3985E1FE0> with id None
Running agent customer_support (turn 2)
Creating span <agents.tracing.span_data.ResponseSpanData object at 0x000001D3985B6790> with id None
Calling LLM gpt-4.1-mini with input:
[
  {
    "content": "i am shoaib, call customer_support_filter tool",
    "role": "user"
  }
]
Tools:
[
  {
    "name": "greeting",
    "parameters": {
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        }
      },
      "required": [
        "name"
      ],
      "title": "greeting_args",
      "type": "object",
      "additionalProperties": false
    },
    "strict": true,
    "type": "function",
    "description": ""
  }
]
Stream: False
Tool choice: NOT_GIVEN
Response format: NOT_GIVEN
Previous response id: None

Exported 5 items
LLM resp:
[
  {
    "arguments": "{\"name\":\"shoaib\"}",
    "call_id": "call_78m0No0oGlRVsIePRcbT72CY",
    "name": "greeting",
    "type": "function_call",
    "id": "fc_686be9b3d7c481988ad9348dd93a53180848a1a8ffec5bfb",
    "status": "completed"
  }
]

Creating span <agents.tracing.span_data.FunctionSpanData object at 0x000001D398F88550> with id None
Invoking tool greeting with input {"name":"shoaib"}
Tool call args: ['shoaib'], kwargs: {}
Tool greeting returned hello nice to meet you shoaib
Running agent customer_support (turn 3)
Creating span <agents.tracing.span_data.ResponseSpanData object at 0x000001D398F82690> with id None
Calling LLM gpt-4.1-mini with input:
[
  {
    "content": "i am shoaib, call customer_support_filter tool",
    "role": "user"
  },
  {
    "arguments": "{\"name\":\"shoaib\"}",
    "call_id": "call_78m0No0oGlRVsIePRcbT72CY",
    "name": "greeting",
    "type": "function_call",
    "id": "fc_686be9b3d7c481988ad9348dd93a53180848a1a8ffec5bfb",
    "status": "completed"
  },
  {
    "call_id": "call_78m0No0oGlRVsIePRcbT72CY",
    "output": "hello nice to meet you shoaib",
    "type": "function_call_output"
  }
]
Tools:
[
  {
    "name": "greeting",
    "parameters": {
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        }
      },
      "required": [
        "name"
      ],
      "title": "greeting_args",
      "type": "object",
      "additionalProperties": false
    },
    "strict": true,
    "type": "function",
    "description": ""
  }
]
Stream: False
Tool choice: NOT_GIVEN
Response format: NOT_GIVEN
Previous response id: None

LLM resp:
[
  {
    "id": "msg_686be9b4ce5481988caf51af4d333b6c0848a1a8ffec5bfb",
    "content": [
      {
        "annotations": [],
        "text": "Hello Shoaib! How can I assist you today? You mentioned calling the customer_support_filter tool. Could you please provide more details on what you need help with?",
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
==========================================================================================
Shutting down trace provider
Shutting down trace processor <agents.tracing.processors.BatchTraceProcessor object at 0x000001D396B29400>
Exported 4 items
PS D:\GOVERNER HOUSE\SIR TAHA CLASSES\PIAIC_AGENTIC_AI_CLasses_Q2\Class_19_handoff_details_Code_2>
