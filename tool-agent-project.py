import sys
from dotenv import load_dotenv

from typing import Literal
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI


load_dotenv()
sys.stdout.reconfigure(encoding="utf-8")


#replica of our db with python dictionary
ORDERS = {
    "ORD-1001":{
        "item":"Wireless mouse",
        "status":"shipped",
        "amount":1499,
        "pin":"400001"
    },
    "ORD-1002":{
        "item":"Mechanical Keyboard",
        "status":"packed",
        "amount":4999,
        "pin":"560034"
    },
}

# pydantic model for tool input to make sure we are not blindly trust argument

class RefundInput(BaseModel):
    #the order id is required
    order_id:str = Field(
        description="Order id, for example ORD-1001",
    )
    # The reason is required and must contain at least 5 characters.
    reason:str = Field(
        description="why the customer wants a refund",
        min_length=5
    )     
    

#tool 1 - check order status

@tool
def order_status(order_id:str)->str:
    """Get the item, status and amount of an order usig its id."""
    order = ORDERS.get(order_id.upper())
    
    # if the order does not exist, return a useful message.
    if order is None:
        return f"No order found with id {order_id}."
    
    #return the information that the agent needs.
    return(
        f"{order['item']}, "
        f"status{order['status']},"
        f"amount{order['amount']} rupees"
    )
    
    
#tool 2 - delivery estimate

@tool
def delivery_estimate(order_id:str)->str:
    """Estimate when an order will be delivered."""
    order = ORDERS.get(order_id.upper())
    if order is None:
        return f"No order found with id {order_id}."
    
    return "2days" if order["pin"].startswith("4") else "5 days"


#tool 3 - Start Refund

@tool("start_refund", args_schema=RefundInput)
def start_refund(order_id:str, reason:str)->str:
    """
    start a refund for an order.
    only use it after the customer clearly asks for one.
    
    """
    
    #check whether the order exists or not
    if order_id.upper() not in ORDERS:
        return f"Cannot refund, no order with id {order_id}."
    
    #if the order exists, start the refund
    return(
        f"Refund started for {order_id.upper()}, "
        f"reason started as : {reason}"
    )
    

#tool 4 - Escalate to Human

@tool
def escalate(order_id:str, note:str)->str:
    """Send the case to a human agent when you cannot solve it."""
    return (
        f"case for {order_id} sent to a human"
        f"with note:{note}"
    )
    
    
# STRUCTURED OUTPUT MODEL

# for example , instead of only:
#         "your orde is packed"
# we can get :
#
#     order_id     -> ORD-1002
#     intent       -> status
#     message      -> Your order is packed.
#     action_taken -> Checked order status
#     needs_human  -> False
    
    
class Reply(BaseModel):
    """Structured result returned by the support agent."""
    
    #which order was discussed?
    order_id:str = Field(description="Order discussed, or NA")
    
    intent:Literal[
        "status",
        "delivery",
        "refund",
        "other"
               ] = Field(description="what the customer wanted")
    message:str = Field(description="The reply to show the customer")
    
    action_taken:str=Field(description="What the agent actually did")
    needs_human: bool = Field( description="True if a person must follow up" )
    
    
llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(
    model=llm,
    tools=[order_status,delivery_estimate,start_refund,escalate],
    system_prompt=(
    "You are the support agent for an online store. "
    "Never invent, assume, or guess an order ID. "
    "If the customer asks about an order but does not provide an order ID, "
    "ask them for the order ID. "
    "Always look up an order before answering about it. "
    "For refunds, only call start_refund when the customer explicitly asks "
    "for a refund AND a valid order ID has been provided or established "
    "in the conversation. "
    "Never use an order ID from another conversation or guess one. "
    "Never guess numbers or dates. "
    "Escalate anything you cannot handle with the tools you have."
    ),
    response_format=Reply,
    checkpointer=InMemorySaver(),
)


conversation = [
"Hi, where is my order ORD-1002?",
"When will it reach me?",
"That is too late, I want a refund because I need it this week."
]

config ={
    "configurable":{
        "thread_id":"brand-new-test-123"
    }
}


for question in conversation:
    result = agent.invoke({
        "messages":[
            {
                "role":"user",
                "content":question
            }
        ]
    },
    config=config
)
    reply = result["structured_response"]
    print("Customer: ", question)
    print("Agent: ", reply.message)
    print()
    print("Application data:")
    print(f" order_id = {reply.order_id}")
    print(f" intent = {reply.intent}")
    print(f" action_taken = {reply.action_taken}")
    print(f" needs_human = {reply.needs_human}")
    print("-"*60)



