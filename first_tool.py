#creating a basic tool
from langchain_core.tools import tool 
from datetime import datetime
from zoneinfo import ZoneInfo

@tool
def multiply(a1:int, a2:int) -> int:
    """Multiply two numbers and return the exact result."""
    return a1*a2

@tool
def current_time(city:str)->str:
    """Get the current time in a city. Use it whenever the user asks about time."""
    zones = {
        "mumbai":"Asia/Kolkata",
        "delhi":"Asia/Kolkata",
        "london":"Europe/London",
        "new york":"America/New_York",
    }
    
    zone = zones.get(city.lower())
    
    if zone is None:
        return f"I dont know the timezone for the {city}."
    
    return datetime.now(ZoneInfo(zone)).strftime("%d %B %Y, %I:%M %p")
    

print(multiply.name)
print(multiply.description)
print(multiply.args)
result1 = current_time.invoke({"city":"new york"})
result2 = multiply.invoke({"a1":2, "a2":2})



print(result1)
print(result2)