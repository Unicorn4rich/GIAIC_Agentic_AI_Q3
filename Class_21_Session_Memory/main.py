from dotenv import load_dotenv
from agents import Agent, Runner, enable_verbose_stdout_logging, SQLiteSession
import rich


#-------------------------------
load_dotenv()
# enable_verbose_stdout_logging()
#------------------------------------

# Is session ke andar wo hmari conversation history ko save karta jaega or usy har cheez yad rhegi jitne bhi runner laga kar alag alag request kar len.
memory = SQLiteSession( session_id="conversation_123", db_path="test.db") # session_id-> ye session ka naam hai or db_path -> ye file bana ke dey dega permanent memory save rakhny ke liye database mein bhaly ham laptop band kar ke wapas bhi on kar ke check kar len data save ho chuka hoga.. 

#------------------------------------

agent = Agent( 
    name="my_agent",
    instructions="You are a helpful assitant",
    model="gpt-4.1-mini",
) 

#------------------------------------

# hamne isko apna naam btaya or isme session memory pass ki to ye hmare naam ko is session id se yad rakhega agr ye nahi dety to wo hmara naam bhool jata reslut dety hi.
result1 =  Runner.run_sync(agent, input="hi i am shoaib", session=memory) 
rich.print(result1.final_output) # Hello Shoaib! How can I assist you today?

# yahn par dosri request karenge to wo naam isko yad hoga pehli request wala.
result2 =  Runner.run_sync(agent, input="do you know me?", session=memory) 
rich.print(result2.final_output) # Hello Shoaib! I don’t have the ability to know personal details about you unless you share them with me. How can I help you today?

#---------------------------------------------------------------------------------------------------------------
# 