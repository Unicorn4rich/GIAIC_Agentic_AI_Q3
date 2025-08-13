from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled, enable_verbose_stdout_logging, trace, TracingProcessor, set_default_openai_api, set_trace_processors
import rich
import asyncio

#-------------------------------
load_dotenv()
# enable_verbose_stdout_logging()
# set_tracing_disabled(disabled=True)

#------------------------------------
# Class for Custom tracing

class My_Local_Trace_Class(TracingProcessor):
    def __init__(self):
        self.traces = []  # tracess ko save karene is local fake database mein.
        self.spans = []   # spans ko save karene is local fake database mein

    def on_trace_start(self, trace):
        self.traces.append(trace)  # trace start hoty hi uska data opar wali traces list mein save krwa deti hai.
        print(f"Trace started: {trace.trace_id}")        

    def on_trace_end(self, trace): # trace end pr print krwaya.
        print(f"Trace ended: {trace.export()}")
        
    def on_span_start(self, span):
        self.spans.append(span)  # span start hoty hi usy opar wali hmari sapns list/fake-database mein save karwa denge
        print(f"Span started: {span.span_id}") # span id terminal mein dikhaye
        print(f"Span details: ")
        rich.print(span.export())        

    def on_span_end(self, span):
        print(f"Span ended: {span.span_id}")
        print(f"Span details:")
        rich.print(span.export())      
     
    def force_flush(self):
        print("Forcing flush of trace data")

    def shutdown(self):
        print("=======Shutting down trace processor========")
        # Print all collected trace and span data
        print("Collected Traces:")
        for trace in self.traces:  # opar wali list/data-base mein jo traces save krwai thi unko loop laga kar dikhaa rhy hain.
            print(trace.export())
        print("Collected Spans:")
        for span in self.spans:    # opar wali list/data-base mein jo spans save krwai thi unko loop laga kar dikhaa rhy hain.
            print(span.export())          
        
#------------------------------------
# configrations custom tracing ko chlany ki.

set_default_openai_api("chat_completions") # by-default hmara agent sdk response api pe chalta hai but ham isy chat_completions mein chlana chahty hain
local_processor = My_Local_Trace_Class() # instance create
set_trace_processors([local_processor])

#------------------------------------

agent = Agent( 
    name="My_agentt",
    instructions="You are a helpful assistant",
    model="gpt-4.1-mini",
) 

#---------------------------------

async def main():
    with trace("Shoaib_Tracing"):
        result = await Runner.run(agent, input="hi, how is the weather of karachi?") 
        # result = await Runner.run(agent, input="who is the shoaib from pakistan?") # jitne bhi runners honge sab aik hi Trace mein save honge.
        rich.print("🙂", result.final_output)
    
asyncio.run(main());    



#---------------------------------------------------------------------------------------------------------------
# Custom Tracing Class Terminal Output:


# PS D:\GOVERNER HOUSE\SIR TAHA CLASSES\GIAIC_Agentic_AI_Q3\Class_17_Tracing> uv run main.py
# Trace started: trace_81e22917a75a402dbc7cfc698f2337b4
# Span started: span_53d14c8b5a7a4b24b14cac92
# Span details:
# {
#     'object': 'trace.span',
#     'id': 'span_53d14c8b5a7a4b24b14cac92',
#     'trace_id': 'trace_81e22917a75a402dbc7cfc698f2337b4',
#     'parent_id': None,
#     'started_at': '2025-08-07T15:53:13.040301+00:00',
#     'ended_at': None,
#     'span_data': {'type': 'agent', 'name': 'My_agentt', 'handoffs': [], 'tools': None, 'output_type': 'str'},
#     'error': None
# }
# Span started: span_f3e3a78d2b42404c9672dfc8
# Span details: 
# {
#     'object': 'trace.span',
#     'id': 'span_f3e3a78d2b42404c9672dfc8',
#     'trace_id': 'trace_81e22917a75a402dbc7cfc698f2337b4',
#     'parent_id': 'span_53d14c8b5a7a4b24b14cac92',        
#     'started_at': '2025-08-07T15:53:13.631827+00:00',    
#     'ended_at': None,
#     'span_data': {
#         'type': 'generation',
#         'input': None,
#         'output': None,
#         'model': 'gpt-4.1-mini',
#         'model_config': {
#             'temperature': None,
#             'top_p': None,
#             'frequency_penalty': None,
#             'presence_penalty': None,
#             'tool_choice': None,
#             'parallel_tool_calls': None,
#             'truncation': None,
#             'max_tokens': None,
#             'reasoning': None,
#             'metadata': None,
#             'store': None,
#             'include_usage': None,
#             'response_include': None,
#             'extra_query': None,
#             'extra_body': None,
#             'extra_headers': None,
#             'extra_args': None,
#             'base_url': 'https://api.openai.com/v1/'
#         },
#         'usage': None
#     },
#     'error': None
# }
# Span ended: span_f3e3a78d2b42404c9672dfc8
# Span details:
# {
#     'object': 'trace.span',
#     'id': 'span_f3e3a78d2b42404c9672dfc8',
#     'trace_id': 'trace_81e22917a75a402dbc7cfc698f2337b4',
#     'parent_id': 'span_53d14c8b5a7a4b24b14cac92',
#     'started_at': '2025-08-07T15:53:13.631827+00:00',
#     'ended_at': '2025-08-07T15:53:16.522311+00:00',
#     'span_data': {
#         'type': 'generation',
#         'input': [{'content': 'You are a helpful assistant', 'role': 'system'}, {'role': 'user', 'content': 'hi, how is the weather of karachi?'}],
#         'output': [
#             {
#                 'content': "Hello! I don't have real-time weather information. To get the current weather in Karachi, you can check a reliable weather website 
# or app like Weather.com, AccuWeather, or use a voice assistant. Is there anything else I can help you with?",
#                 'refusal': None,
#                 'role': 'assistant',
#                 'annotations': [],
#                 'audio': None,
#                 'function_call': None,
#                 'tool_calls': None
#             }
#         ],
#         'model': 'gpt-4.1-mini',
#         'model_config': {
#             'temperature': None,
#             'top_p': None,
#             'frequency_penalty': None,
#             'presence_penalty': None,
#             'tool_choice': None,
#             'parallel_tool_calls': None,
#             'truncation': None,
#             'max_tokens': None,
#             'reasoning': None,
#             'metadata': None,
#             'store': None,
#             'include_usage': None,
#             'response_include': None,
#             'extra_query': None,
#             'extra_body': None,
#             'extra_headers': None,
#             'extra_args': None,
#             'base_url': 'https://api.openai.com/v1/'
#         },
#         'usage': {'input_tokens': 26, 'output_tokens': 51}
#     },
#     'error': None
# }
# Span ended: span_53d14c8b5a7a4b24b14cac92
# Span details:
# {
#     'object': 'trace.span',
#     'id': 'span_53d14c8b5a7a4b24b14cac92',
#     'trace_id': 'trace_81e22917a75a402dbc7cfc698f2337b4',
#     'parent_id': None,
#     'started_at': '2025-08-07T15:53:13.040301+00:00',
#     'ended_at': '2025-08-07T15:53:16.554886+00:00',
#     'span_data': {'type': 'agent', 'name': 'My_agentt', 'handoffs': [], 'tools': [], 'output_type': 'str'},
#     'error': None
# }
# 🙂 Hello! I don't have real-time weather information. To get the current weather in Karachi, you can check a reliable weather website or app like Weather.com, 
# AccuWeather, or use a voice assistant. Is there anything else I can help you with?
# Trace ended: {'object': 'trace', 'id': 'trace_81e22917a75a402dbc7cfc698f2337b4', 'workflow_name': 'Shoaib_Tracing', 'group_id': None, 'metadata': None}
# =======Shutting down trace processor========  ->>> iske neechy jo bhi likha hua hai wo sab hamne jama kiyya hai apne pass list/data-base mein save kar liya inko.
# Collected Traces:
# {'object': 'trace', 'id': 'trace_81e22917a75a402dbc7cfc698f2337b4', 'workflow_name': 'Shoaib_Tracing', 'group_id': None, 'metadata': None}
# Collected Spans:
# {'object': 'trace.span', 'id': 'span_53d14c8b5a7a4b24b14cac92', 'trace_id': 'trace_81e22917a75a402dbc7cfc698f2337b4', 'parent_id': None, 'started_at': '2025-08-07T15:53:13.040301+00:00', 'ended_at': '2025-08-07T15:53:16.554886+00:00', 'span_data': {'type': 'agent', 'name': 'My_agentt', 'handoffs': [], 'tools': [], 'output_type': 'str'}, 'error': None}
# {'object': 'trace.span', 'id': 'span_f3e3a78d2b42404c9672dfc8', 'trace_id': 'trace_81e22917a75a402dbc7cfc698f2337b4', 'parent_id': 'span_53d14c8b5a7a4b24b14cac92', 'started_at': '2025-08-07T15:53:13.631827+00:00', 'ended_at': '2025-08-07T15:53:16.522311+00:00', 'span_data': {'type': 'generation', 'input': [{'content': 'You are a helpful assistant', 'role': 'system'}, {'role': 'user', 'content': 'hi, how is the weather of karachi?'}], 'output': [{'content': "Hello! I don't 
# have real-time weather information. To get the current weather in Karachi, you can check a reliable weather website or app like Weather.com, AccuWeather, or use a voice assistant. Is there anything else I can help you with?", 'refusal': None, 'role': 'assistant', 'annotations': [], 'audio': None, 'function_call': None, 'tool_calls': None}], 'model': 'gpt-4.1-mini', 'model_config': {'temperature': None, 'top_p': None, 'frequency_penalty': None, 'presence_penalty': None, 'tool_choice': None, 'parallel_tool_calls': None, 'truncation': None, 'max_tokens': None, 'reasoning': None, 'metadata': None, 'store': None, 'include_usage': None, 'response_include': None, 'extra_query': None, 'extra_body': None, 'extra_headers': None, 'extra_args': None, 'base_url': 'https://api.openai.com/v1/'}, 'usage': {'input_tokens': 26, 'output_tokens': 51}}, 'error': None}
# PS D:\GOVERNER HOUSE\SIR TAHA CLASSES\GIAIC_Agentic_AI_Q3\Class_17_Tracing> 