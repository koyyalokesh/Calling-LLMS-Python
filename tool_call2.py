#picks between two tools by reading the descriptions

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

@tool
def multiply(a:float, b:float)->float:
    """Multiply of numbers"""
    return a*b


@tool
def words_count(text:str)->int:
    """Count words in a text"""
    return len(text.split())


llm_with_tools = llm.bind_tools([multiply, words_count])

#it picked the right one out of two, from the descriptions alone

response = llm_with_tools.invoke("product of 2 and 6.")

print(response.tool_calls)