from dotenv import load_dotenv
from agents import Agent, Runner, TResponseInputItem, set_tracing_disabled, enable_verbose_stdout_logging
import rich
from agents.run import AgentRunner, set_default_agent_runner
import asyncio

#-------------------------------
load_dotenv()
# enable_verbose_stdout_logging()
# set_tracing_disabled(disabled=True)

#------------------------------------
# Class

class MyCustomRunClass(AgentRunner):  # AgentRunner -> final_output mein jo jawab ata hai usko ham yahn se modify kar sakty hain is class se.
    async def run(self, starting_agent: Agent, input: str | list[TResponseInputItem], **kwargs): # kwargs -> isme extra cheezen ati hain jitni chahy jese max_turn session, context etc.
        
        response = await super().run(starting_agent, input, **kwargs) # RunResult return aa rha hai isme se.
        response.final_output = "My name is shoaib"
        return response


set_default_agent_runner(MyCustomRunClass())
#------------------------------------

agent = Agent( 
    name="my_agent",
    instructions="You are a helpful assitant",
    model="gpt-4.1-mini"
) 

#------------------------------------

async def main():
    result = await Runner.run(agent, input="hi") 
    rich.print(result.final_output)  # My name is shoaib -> RunResult ki kisi bhi property ko modify kar sakty hain jese output ko kiyya hai.
    # rich.print(result) # All agent propertys
    # rich.print(result.raw_responses[0].output[0].content[0].text) # is aega to final_output ka jawab but ham strucre dekh rhy hain.

asyncio.run(main())



#------------------------------------------------------------------------------------------------------------
# Runner.run RUnResult return karta hai

# RunResult(
#     input='hi',
#     new_items=[
#         MessageOutputItem(
#             agent=Agent(
#                 name='my_agent',
#                 handoff_description=None,
#                 tools=[],
#                 mcp_servers=[],
#                 mcp_config={},
#                 instructions='You are a helpful assitant',
#                 prompt=None,
#                 handoffs=[],
#                 model='gpt-4.1-mini',
#                 model_settings=ModelSettings(
#                     temperature=None,
#                     top_p=None,
#                     frequency_penalty=None,
#                     presence_penalty=None,
#                     tool_choice=None,
#                     parallel_tool_calls=None,
#                     truncation=None,
#                     max_tokens=None,
#                     reasoning=None,
#                     metadata=None,
#                     store=None,
#                     include_usage=None,
#                     response_include=None,
#                     extra_query=None,
#                     extra_body=None,
#                     extra_headers=None,
#                     extra_args=None
#                 ),
#                 input_guardrails=[],
#                 output_guardrails=[],
#                 output_type=None,
#                 hooks=None,
#                 tool_use_behavior='run_llm_again',
#                 reset_tool_choice=True
#             ),
#             raw_item=ResponseOutputMessage(
#                 id='msg_689cc5ee9228819e9584867423444eab0a5aef61b733a04a',
#                 content=[ResponseOutputText(annotations=[], text='Hello! How can I assist you today?', type='output_text', logprobs=[])],
#                 role='assistant',
#                 status='completed',
#                 type='message'
#             ),
#             type='message_output_item'
#         )
#     ],
#     raw_responses=[
#         ModelResponse(
#             output=[
#                 ResponseOutputMessage(
#                     id='msg_689cc5ee9228819e9584867423444eab0a5aef61b733a04a',
#                     content=[ResponseOutputText(annotations=[], text='Hello! How can I assist you today?', type='output_text', logprobs=[])],
#                     role='assistant',
#                     status='completed',
#                     type='message'
#                 )
#             ],
#             usage=Usage(
#                 requests=1,
#                 input_tokens=18,
#                 input_tokens_details=InputTokensDetails(cached_tokens=0),
#                 output_tokens=10,
#                 output_tokens_details=OutputTokensDetails(reasoning_tokens=0),
#                 total_tokens=28
#             ),
#             response_id='resp_689cc5ee1b08819eb2fb0f3678df4add0a5aef61b733a04a'
#         )
#     ],
#     final_output='Hello! How can I assist you today?',
#     input_guardrail_results=[],
#     output_guardrail_results=[],
#     context_wrapper=RunContextWrapper(
#         context=None,
#         usage=Usage(
#             requests=1,
#             input_tokens=18,
#             input_tokens_details=InputTokensDetails(cached_tokens=0),
#             output_tokens=10,
#             output_tokens_details=OutputTokensDetails(reasoning_tokens=0),
#             total_tokens=28
#         )
#     ),
#     _last_agent=Agent(
#         name='my_agent',
#         handoff_description=None,
#         tools=[],
#         mcp_servers=[],
#         mcp_config={},
#         instructions='You are a helpful assitant',
#         prompt=None,
#         handoffs=[],
#         model='gpt-4.1-mini',
#         model_settings=ModelSettings(
#             temperature=None,
#             top_p=None,
#             frequency_penalty=None,
#             presence_penalty=None,
#             tool_choice=None,
#             parallel_tool_calls=None,
#             truncation=None,
#             max_tokens=None,
#             reasoning=None,
#             metadata=None,
#             store=None,
#             include_usage=None,
#             response_include=None,
#             extra_query=None,
#             extra_body=None,
#             extra_headers=None,
#             extra_args=None
#         ),
#         input_guardrails=[],
#         output_guardrails=[],
#         output_type=None,
#         hooks=None,
#         tool_use_behavior='run_llm_again',
#         reset_tool_choice=True
#     )
# )
# (class-17-tracing) PS D:\GOVERNER HOUSE\SIR TAHA CLASSES\GIAIC_Agentic_AI_Q3\Class_22_Custom_Runner>




























