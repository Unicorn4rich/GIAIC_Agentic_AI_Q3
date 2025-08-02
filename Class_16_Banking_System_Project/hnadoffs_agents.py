from agents import Agent
from output_guardrail import res_check



#------------------------------------
# specialist handoffs agents

account_agent = Agent( 
    name="Account Services Agent",
    instructions="You help user in their query of account balance, statement, and account information, always create a token!. ",
    model="gpt-4.1-mini",
    output_guardrails=[res_check]
) 

transfer_agent = Agent( 
    name="Transfer Services Agent",
    instructions="You help user with money transfer and payments, always create a token!. ",
    model="gpt-4.1-mini",
    output_guardrails=[res_check]
) 

loan_agent = Agent( 
    name="Loan Services Agent",
    # instructions="You help user with loans and mortgages, always create a token!. ",
    instructions="never reply according to banking . ",
    model="gpt-4.1-mini",
    output_guardrails=[res_check]
) 
