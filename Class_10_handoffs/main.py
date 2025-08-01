from dotenv import load_dotenv
from agents import Agent, Runner
import rich


#-------------------------------
load_dotenv()
#---------------------------------

triage_agent = Agent( 
    name="triage_agent",
    instructions="when ever user ask for weather you use tool for fetching weather data, you are a helpful assitant.",
    model="gpt-4.1-mini", 
)  
  
#-------------------------------
result =  Runner.run_sync(triage_agent, input="hi how are you") 
rich.print(result.final_output)

#-------------------------------------------------------------------------------------------------------------------
# Notes:


