
from dotenv import load_dotenv # type: ignore
from agents import Agent, Runner, ModelSettings # type: ignore

load_dotenv()

agent = Agent(
    model="gpt-4.1-mini",
    name="my_aent",
    instructions="You are a helpful asisstent, always search in file for information",
    model_settings=ModelSettings(temperature=0.1) # minimum temperature pe aik jesa consistant jawab milta hai.
    model_settings=ModelSettings(temperature=1)   # maximum temperature pe zyada creative jawab milta hai har dafa alag alag.
    # agr ham ye nahi likhty to by-default (temperature=0.7) hota hai. 
    # maximum temperature 1 hota hai or minimum 0.1 hota hai. 
    # temperature jitna km hoga ye utna consistant bagher sochy samjhy jawab dega or agr temperature high hoga to ye soch samjh kar har dafa alag alag jawab dega.
    model_settings=ModelSettings(temperature=1, max_tokens=1000) # iska matlab ye hai ke ye LLM (thousand) tokens tak chalega phir ye limit laga dega nahichalega.
)

#----------------------------------------------------------------------------
res = Runner.run_sync(agent, 'Who are you?') 
print(res.final_output)

# if you want to buy openAi Key then you go to (platform.openai.com) and you get the key there. but you can pay money
# by international cards like (naya pay) (sada pay) and other international cards.