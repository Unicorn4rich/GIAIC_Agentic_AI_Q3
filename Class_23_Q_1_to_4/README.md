Level 1 Prepration

You want two separate Runner.run() calls to be part of the same trace session named "JokeWorkflow". How should you do this?

Wrap both Runner.run(...) invocations inside a with trace("JokeWorkflow"): block. ← (Correct Answer)

Pass trace="JokeWorkflow" into both run() calls individually.

Use the group_id parameter in Runner.run(...) to label both runs identically.

Manually merge trace files after both runs complete.


----------------------------------------------------------------------


What is the purpose of the resolve() method within ModelSettings?

Combines default settings with overrides and returns a new settings instance. ← (Correct Answer)

Immediately sends settings to the LLM API.

Validates if all required settings are non-null.

Deletes unset fields and returns the same object.

---------------------------------------------------------------------

You want your target agent to only receive the last 2 messages from history when a handoff occurs. Which handoff parameter helps with this?

tool_name_override

tool_description_override

input_filter ← (Correct Answer)

on_handoff

---------------------------------------------------------------------

@function_tool
def analyze_portfolio(symbols: List[str]) -> dict:
    results = {}
    for symbol in symbols:
        try:
            data = get_stock_data(symbol)  # May fail for invalid symbols
            analysis = perform_analysis(data)
            results[symbol] = analysis
        except Exception as e:
            results[symbol] = f"Error: {str(e)}"
    return results




The agent receives mixed results with some symbols having analysis data and others having error strings. It then tries to parse all results as analysis data, leading to errors on error strings. What's the more sophisticated approach to handle this mixed success/failure scenario?

Return only successful results and ignore failed ones

Use a structured result format with success/failure indicators and separate error details ← (Correct Answer)

Raise an exception if any symbol fails to maintain data consistency

Log errors and return empty results for failed symbols

---------------------------------------------------------------------

By default, if you set output_type=BarModel (a Pydantic model) and do not specify output_schema_unified, the SDK will generate a valid JSON schema.

True ← (Correct Answer)

False

Only if you used StrictInt or StrictStr in BarModel

Only if you passed convert_schemas_to_strict=True to the Agent

---------------------------------------------------------------------

One of Pydantic’s standout features is that it uses Python type hints for data validation and schema definition. Why is this powerful?

They allow seamless validation, integrate with IDEs and static type-checkers like MyPy or Pyright. ← (Correct Answer)

Type hints are optional and don’t affect validation.

Type hints allow storing runtime values inside models.

Type hints ensure Pydantic will bypass all validation if annotations match.

----------------------------------------------------------------------

In a banking chatbot, you want to ensure that before any transaction request is processed, the system verifies that the amount provided is a valid number and doesn’t exceed the user’s daily transfer limit. Which scenario best demonstrates the essential use of an input guardrail?

Ensuring the chatbot’s output is polite and well-mannered before displaying it to the user.

Blocking the chatbot from connecting to unauthorized external banking APIs during execution.

Validating that the requested transfer amount is a valid positive integer and below the allowed daily maximum before the agent attempts the transaction. ← (Correct Answer)

Shortening overly long user messages to conserve tokens before the agent processes them.

----------------------------------------------------------------------

You have an orchestrator agent that uses 5 specialist agents as tools. During execution, one specialist agent (translation agent) encounters an API rate limit and fails. The orchestrator’s instructions include “If any translation fails, try an alternative approach.”
What happens to the orchestrator’s execution context and the remaining specialist agents?

The orchestrator immediately fails with the specialist’s exception, and all pending tool calls are cancelled.

The orchestrator receives the exception as tool output, can handle it in its reasoning, and continues with other specialists. ← (Correct Answer)

The failed specialist automatically retries 3 times before the orchestrator sees the failure.

All specialist agents share the same execution context, so the failure affects all of them.

----------------------------------------------------------------------

A developer implements handoffs like this:

# In data_agent tools
@function_tool
def handoff_to_analyzer(data: str):
    return analysis_agent  # This seems logical

The system fails unpredictably in production. What's the subtle but critical issue with this handoff pattern?

Handoffs should use the Handoff class, not return agent objects directly. ← (Correct Answer)

The data parameter should be a complex object, not a string.

Each agent needs identical tool sets for handoffs to work.

Agents can't handoff to each other without a coordinator agent.

----------------------------------------------------------------------

When using a low temperature (e.g., 0.3), a moderate top_k (e.g., 50), and a high top_p (e.g., 0.95), what kind of output is most likely?

Very random, with lots of strange word choices

Creative and varied, but still coherent

Extremely focused and repetitive ← (Correct Answer)

Completely deterministic with no variety

A low temperature makes the model's output more deterministic and focused, often resulting in repetitive responses, even if top_k and top_p are set to allow more variety.

----------------------------------------------------------------------

Which code snippet allows you to define dynamic instructions for an agent, based on the context?

Agent(ChatCtx)(name="Chat", instructions="Hello, {name}, how can I help?")

Agent(ChatCtx)(name="Chat", instructions=lambda ctx, ag: f"Hi {ctx.context.name}, your last message: {ctx.context.last_msg}")

def dyn(ctx: RunContextWrapper[ChatCtx], ag: Agent): return f"Name: {ctx.context.name}"
Agent(ChatCtx)(name="Chat", instructions=dyn) ← (Correct Answer)

Agent(ChatCtx)(name="Chat", instructions=ChatCtx)

----------------------------------------------------------------------

You want your target agent to only receive the last 2 messages from history when a handoff occurs. Which handoff() parameter helps with this?

tool_name_override

tool_description_override

input_filter ← (Correct Answer)

on_handoff

----------------------------------------------------------------------

What happens when a guardrail tripwire is triggered?

The agent logs a warning but continues processing

A GuardrailTripwireTriggered exception is raised, stopping agent execution ← (Correct Answer)

The agent automatically retries the same prompt

The next agent in the workflow takes over

----------------------------------------------------------------------

You create a custom tool with error handling:

@function_tool
def risky_operation(data: str) -> str:
    if data == "fail":
        raise ValueError("Operation failed!")
    return f"Success: {data}"

agent = Agent(
    name="Test Agent",
    instructions="Use the risky tool. If it fails, try again with `retry` as input.",
    tools=[risky_operation]
)

result = Runner.run_sync(agent, "Please use risky_operation with input 'fail'")


What happens when the tool raises ValueError?

The agent execution stops with an unhandled ValueError, terminating the conversation

The agent receives the error message as tool output and can retry based on its instructions ← (Correct Answer)

The SDK automatically retries the tool call 3 times before failing

The tool call is skipped and the agent responds without using any tools

----------------------------------------------------------------------

You have an orchestrator agent that uses 5 specialist agents as tools. During execution, one specialist agent (translation_agent) encounters an API rate limit and fails. The orchestrator’s instructions include “If any translation fails, try an alternative approach.”
What happens to the orchestrator’s execution context and the remaining specialist agents?

The orchestrator immediately fails with the specialist’s exception, and all pending tool calls are cancelled

The orchestrator receives the exception as tool output, can handle it in its reasoning, and continues with other specialists ← (Correct Answer)

The failed specialist automatically retries 3 times before the orchestrator sees the failure

All specialist agents share the same execution context, so the failure affects all of them

----------------------------------------------------------------------

@function_tool
def get_weather(city: str) -> str:
    # Simulates weather API call
    return f"Weather in {city}: 25°C, sunny"

agent = Agent(
    name="Weather Assistant",
    instructions="You are a helpful weather assistant. Use the weather tool when users ask for weather information.",
    tools=[get_weather]
)

# Test with max_turns=1
result = Runner.run_sync(agent, "Hello, what can you do?", max_turns=1)
print(result.final_output)


What will be the output of this code and why?

The agent raises a MaxTurnsException and fails to provide any response. This is as agent loop needs 2 LLM calls: one to analyze the request and call tools, another to process tool results and respond

The agent successfully responds with: "I'm a weather assistant! This is a direct response without using tools, requiring only 1 LLM call which fits within max_turns=1" ← (Correct Answer)

max_turns=1 only applies to tool calls, not to regular conversational responses

The weather tool was called and we will get the direct tool call result 'Weather in Karachi: 25°C, sunny.'

----------------------------------------------------------------------

If you want to log whenever your agent starts or finishes using a tool, where should you attach your AgentHooks?

Create an AgentHooks instance and pass it into RunHooks when running the agent.

Assign your custom AgentHooks to the hooks attribute of the Agent before running it. ← (Correct Answer)

Modify the RunHooks class to include your AgentHooks methods.

Use the RunContextWrapper to register your AgentHooks during execution.

----------------------------------------------------------------------

What is the effect of using high temperature (e.g., 1.2) with low top_k (e.g., 5) and low top_p (e.g., 0.3)?

Output will be highly unpredictable and full of odd word choices

Very stable but limited—choosing from only a few top tokens

Balanced mix of randomness within a small set of top picks

Identical outputs every time with no creativity ← (Correct Answer)

----------------------------------------------------------------------

Suppose you have a synchronous Python function analyze_portfolio(data: dict) -> str that processes financial data, but your OpenAI Agents SDK workflow is fully asynchronous. What’s the best practice for exposing this synchronous function as a tool in your async-first agent?

Just decorate it with @function_tool; the SDK will automatically handle running it, so your async event loop isn’t blocked.

Manually wrap analyze_portfolio inside an async def that calls await asyncio.to_thread(...), then decorate the wrapper with @function_tool. ← (Correct Answer)

Rewrite the entire function to be async; the SDK doesn’t support synchronous functions at all.

Use a special @sync_function_tool decorator that OpenAI provides for synchronous functions.

----------------------------------------------------------------------

How should you configure instructions so it dynamically updates based on the user’s subscription status at runtime?

Pass a template string like instructions="You are a support agent. User type: {is_premium}" and the SDK will auto-fill {is_premium} from context.

Subclass Agent and override a protected method like _get_dynamic_instructions(self, context). ← (Correct Answer)

Provide the function premium_instructions directly to the instructions argument—since it accepts (context, agent) and returns the proper string.

Dynamic instructions aren’t supported; instructions must be a fixed string at agent creation.