#tool calling loop

from dotenv import load_dotenv
import sys
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from zoneinfo import ZoneInfo
from datetime import datetime
from langchain_core.messages import HumanMessage, SystemMessage
load_dotenv()

sys.stdout.reconfigure(encoding="utf-8")

@tool
def current_time(city:str) -> str:
    """Get the current time in a city."""
    Zones = {
        "mumbai":"Asia/kolkata",
        "london":"Europe/London",
        "new york":"America/New_York"
    }
    
    zone = Zones.get(city.lower())
    if zone is None:
        return f"I do not know the timezone for {city}"
    
    return datetime.now(ZoneInfo(zone)).strftime("%d %B %Y, %I:%M %p")

@tool
def multiply(a:int,b:int)->int:
    """Multiply two numbers and return the exact result."""
    return a*b


#put our tools into a list
tools = [current_time, multiply] 

# we need the name the LLM gives us to find the actual python tool

tools_by_name = {t.name:t for t in tools}

model = ChatOpenAI(
    model = "gpt-4o-mini",
    temperature=0
).bind_tools(tools)

#create the conversation
messages = [
    SystemMessage(
        content="You are a helpful assistant. Use the tools when they fit."
    ),
    HumanMessage(
        content="what time is it in mumbai, and what is 98765 times 43210?"
    ),
]

step =1 

while True:
    response = model.invoke(messages)
    
    #keep the model's own reply in the conversation,
    #so the next turn knows what it already said
    
    messages.append(response)
    
    if not response.tool_calls:
        print("\nFinal answer:")
        print(response.content)
        break
    
    print(f"step {step}: the model asked for {len(response.tool_calls)} tool calls(s)")
    
    for call in response.tool_calls:
        
        #call contains: tool name, arguments, tool call id
        
        tool_to_run = tools_by_name[call["name"]]
        
        # passing the whole call back gives a ToolMessage that is already
        # tied to this request by its id
        
        tool_message = tool_to_run.invoke(call)
        
        print(f" {call['name']}({call['args']}) -> {tool_message.content}")
        
        messages.append(tool_message)
        
    step+=1
    
print("\nMessages in the conversation:", [type(m).__name__ for m in messages])

print(messages)