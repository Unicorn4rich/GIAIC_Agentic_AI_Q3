import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled
import chainlit as cl


load_dotenv()
set_tracing_disabled(disabled=True)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

#------------------------------------
history = []
#------------------------------------

models = {
    "Gemini 2.0 Flash": "google/gemini-2.0-flash-exp:free",
    "Qwen3 14B": "qwen/qwen3-14b:free",
    "Mistral Nemo": "mistralai/mistral-nemo:free",
    "Llama 4 Maverick": "meta-llama/llama-4-maverick:free",
    "Dolphin3.0 Mistral 24B ": "cognitivecomputations/dolphin3.0-mistral-24b:free",
    }

#------------------------------------
@cl.on_chat_start
async def start_message():
    await cl.Message(content="How are my name is shoaib...😁").send()
    
    settings = await cl.ChatSettings(
        [
            cl.input_widget.Select(
                id = "Model",
                label = "Choose any LLM Model",
                values = list(models.keys()),
                initial_index = 0 # ye hmare sary LLMs ke naam show karega.
            )
        ]
        ).send()
    
    await setup_chat(settings)
    
    
#------------------------------------
@cl.on_settings_update
async def setup_chat(settings):
    model_name = settings["Model"]
    cl.user_session.set("model", models[model_name]) # koi sa bhi naam select karenge to wo session mein jaa kar save ho jaega.
    
    await cl.Message(content=f"You have selected {model_name} AI Model").send()
    
#------------------------------------
@cl.on_message
async def my_message(message: cl.Message):
    user_input = message.content
    history.append({"role": "user", "content": user_input})
    
    selected_model = cl.user_session.get("model")
    
    client = AsyncOpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )

    agent = Agent(
        name="my_agent",
        instructions="You are a helpful assistant",
        model=OpenAIChatCompletionsModel(model=selected_model, openai_client=client)
    )    
    
    result = Runner.run_sync(agent, history)
    await cl.Message(content=result.final_output).send()


# for run chainlit code => uv run chainlit run main.py -w  