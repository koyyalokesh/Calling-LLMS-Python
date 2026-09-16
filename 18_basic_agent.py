#langchain agent 

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from datetime import datetime
from zoneinfo import ZoneInfo

load_dotenv()

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


llm = ChatOpenAI(model="gpt-4o-mini")

agent = create_agent(
    model=llm,
    tools=[current_time, multiply],
    system_prompt =(
        "You are a helpful assistant. use tools when they are fit"
    ),
)

result = agent.invoke({
    "messages":[
        {
            "role":"user",
            "content":"who is narendra modi."
        }
    ]
})

print(result["messages"][-1].content)