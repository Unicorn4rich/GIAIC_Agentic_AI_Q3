import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, ModelSettings
import rich


#-------------------------------
load_dotenv()
set_tracing_disabled(disabled=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#-------------------------------

client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

#-------------------------------

shopping_agent = Agent(
    name="shopping_agent",  # Never space in Agent name use underscore.
    instructions="You assist users to finding products and making purchase decisions.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash-lite", openai_client=client),
    handoff_description="a shopping agent to help user in shopping" 
)
#-------------------------------

support_agent = Agent(
    name="support_agent",   # Never space in Agent name use underscore.
    instructions="You help user with post-purchase support and returns.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash-lite", openai_client=client),
    handoff_description="a support agent to help user in post-purchase queries." # handoff_description -> ye ham isliye likhte hain ke jab ye agent kisi dosry agent ko handoff karega to wo description use karega.
)

#-------------------------------

triage_agent = Agent( 
    name="triage_agent",
    instructions=(
        "You are a triage agent,   You delegate task to appropriate agent or use appropriate given tools"
        "When user ask for shopping related query,   You always use given tools"
        "You never reply on your own,   always use given tool to reply user"
        ),
    
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash-lite", openai_client=client),
    
    tools=[ # ye tools ko call karne ke liye use hota hai.
        shopping_agent.as_tool(  # ye agent jisko tool bana kar pass kiyya gaya hai ye tab call hoga jab user shopping se related koi query karega.
            tool_name="transfer_to_shopping_agent", # yahn ham agent ke name se pehly transfer_to likh denge.
            tool_description="You assist user to finding products and making purchase decisions. always add this 😎 emojis in your reply, start reply with this 😎 emoji." # same opar wali instructions pass copy past ki hain but jo extra lines likhi hain ye isliye likhi hain ke output ke time hamen pata chal saky ke konse agent tool chala or hmara kaam kar ke laa kar diyye.
        ),
        
        support_agent.as_tool(  # ye agent jisko tool bana kar pass kiyya gaya hai ye tab call hoga jab user support se related koi query karega.
            tool_name="transfer_to_support_agent", # yahn ham agent ke name se pehly transfer_to likh denge.
            tool_description="You help user with post-purchase support and returns. always add this 🤬 emojis in your reply, start reply with this 🤬 emoji." # same opar wali instructions pass copy past ki hain but jo extra lines likhi hain ye isliye likhi hain ke output ke time hamen pata chal saky ke konse agent tool chala or hmara kaam kar ke laa kar diyye.
        )
    ],
    
    # model_settings=ModelSettings(tool_choice="auto"),    # tool_choice="auto" -> ye agent khud decide karega ke kaunsa tool call karna hai.
    # model_settings=ModelSettings(tool_choice="none"),    # tool_choice="none" -> ye agent tools ko call nahi karega or sirf user se baat karega. 
    model_settings=ModelSettings(tool_choice="required"),  # tool_choice="required" -> ye agent tools ko lazim call karega or agar koi tool nahi mila to error dega.
)

#-------------------------------

# Runner ka jo result hai wo Run_Result mein jawab laa kar return mein deta hai.
result = Runner.run_sync(starting_agent=triage_agent, input="I want to buy a new phone and return my shoes becuse they are not fitting", max_turns=10) # max_turns=10 -> karta ye hai ke agent or llm ke beech jitni dafa chakkar lagenge unko validate karta hai. agr maxturns 10 hai to 10 dafa tak agent or llm ke beech chakkar lagega agr 2 hai to sirf 2 dafa or agr 1 hai to error aega kiyun ke agent jab tak 1 dafa apne tools or user question ley kar jaega tab tak 1 maxturn pora ho jaega.
# rich.print(result.last_agent.name) # reply triage_agent dey rha hai kiyun ke as_tool mein hmesha jawab ye khud ke pass lata hai tools se or user ko btata hai.
rich.print(result.final_output)


# Prompts for use tool_agents:
# 1. I want to purchase shoes -> shopping_agent
# 2. I want your help to return my product -> support_agent
# 3. I want to buy a new phone and return my shoes becuse they are not fitting -> shopping_agent, support_agent -> 2no tool_agents aik sath chalenge paralel pe.



#-------------------------------# Notes: -------------------------------------

# HandsOff or agent ko as_tool bana kar pass karne mein kya defrence hai ? -> controls ka faraq hai.

# 1. answer -> handsoff mein jab main triage_agent task kisi dosry agent ko handoff karta hai to wo agent phir is 
#    triage_agent ko hata kar khud iski jagah par aa jata hai or user se direct ho jata hai or user ko answer karta hai uski query solve kar ke. 

# 2. answer -> Lekin agar ham Agent ko as_tool bana kar pass karte hain triage_agent ko to sara control triage_agent ke pass hi rehta hai 
#    or agent tools se jo bhi answer aega wo is triage_agent ke pass return aega or ye phir user ko dega. iska faida ye hai ke history maintain rehti hai.


# 1. Agent ko jab user kisi cheez ka input deta hai wo input kisi tool_function se related hota hai to ye agentus
#    tool_function agent ko call karta hai or us se khud jawab ley kar user ko deta hai.

# 2. But handsoff mein agr user question karta hai to main agent dosry agent ko handsoff dey deta hai or khud
#    hat jata jata hai or wo handsoff wala agent khud user se direct baat cheet kar ke usy answer karta hai.

# 3. Agent to LLM ke beech jitni dafa chakkar lagenge unko validate karta hai max return 10.
# 4. custom_output_extractor: Callable[[RunResult], Awaitable[str]] | None = None,

# 5. synitizer ya synthitizer jawab ko or behtar bnana -> ye bhi aik agent ka naam rakhty hain or wo agent karta ye hai ke 
#    agr triage_agent kisi agent_tool ko koi task deta hai or wo agent_tool us task ko kar ke wapas triage_agent ko jawab deta to
#    triage_agent us jawab se satisfied nahi hota to wo  apne dosry agent_tool ko bhi call kar sakta hai jese ham aik or agent bana dety hain
#    synthitizer ka or wo synthitizer agent triage_agent ka diyya hua task behtar bnata hai or phir wo triage_agent ko wapas jawab  dey deta hai user ko deny ke liye. 

  
# 6. 2no tools aik sath bhi calls kar sakta hai paralel or jawab dega hamen
# 7. max_turns=2 and 10 ->  tool calling 2 dafa hoti hai or maximum 10 hota hai ->  max_turns bydefault 10 hota hai
# 8. One AI ivocation = 1 max_turn -> MaxTurnExceeded = max turn error
# 9.  tool_choice=none -> not use tools
# 10. tool_choice=auto -> khud ki marzi se tool calls
# 11. tool_choice=required -> tool use lazim karna hai konse ko karna hai apni marzi uski


#----------------------------------------------------------------------------
# triage_agent mein instruction likhne ka tareeqa

    # instructions=(
    #     "persona,             work"
    #     "working condition,   what you do in the condition"
    #     "what not to do,      tool suggestion to use always"
    #     ),



# error when tool call set on none:
# model_settings=ModelSettings(tool_choice="none")

# Use the shopping tool to find a phone
# print(shopping_tool.find_products(query="phone"))
# Use the shopping tool to process the return    
# print(shopping_tool.return_item(item="shoes"))  