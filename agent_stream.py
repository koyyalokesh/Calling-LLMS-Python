#agent working with stream
#lets you watch the agent loop

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

@tool
def ticket_price(city:str)->int:
    """get the flight ticket price in rupees from mumbai to a city."""
    prices = {
                "delhi":4500,
                "bengaluru":3900,
                "kolkata":5200
            }
    return prices.get(city.lower(), 6000)

@tool
def hotel_price(city:str, nights:int)->int:
    """Get the total hotel cost in rupees for a number of nights in a city."""
    per_night = {"delhi":3000, "bengaluru":3500, "kolkata":2800}
    return per_night.get(city.lower(),3200)*nights

agent = create_agent(
    model=llm,
    tools=[ticket_price, hotel_price],
    system_prompt="You plan small trips and always look up real numbers with the tools."
)

question = "I want to go to Bengaluru for 3 nights from mumbai.what is my total cost?"

for chunk in agent.stream(
    {"messages":[{"role":"user","content":question}]},
    
):
    
    for node, update in chunk.items():
        for message in update["messages"]:
            if getattr(message, "tool_calls", None):
                print(f"[{node}] wants: {[c['name'] for c in message.tool_calls]}")
                
            elif type(message).__name__ == "ToolMessage":
                print(f"[{node}] {message.name} returned : {message.content}")
                
            elif message.content:
                print(f"[{node}] says : {message.content}")