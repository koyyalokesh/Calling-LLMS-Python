#Manual Tool Calling Loop

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
load_dotenv()


llm = ChatOpenAI(model="gpt-4o-mini")

#1. Create the tool

@tool
def multiply(a:float, b:float) -> float:
    """Multiply two numbers."""
    return a*b


#2.give the tool to LLM
llm_with_tools = llm.bind_tools([multiply])


#3.Send User's Question
user_message = "multiply of 2 and 4"
response = llm_with_tools.invoke(user_message)

#4.get the tool call requested by the LLM
tool_call = response.tool_calls[0]

#5.Execute the tool
tool_result = multiply.invoke(tool_call["args"])

#6. create a tool message containing the result
tool_message = ToolMessage(
      content = str(tool_result),
      tool_call_id = tool_call["id"]
)

#7.send original conversation + tool result back to LLM
final_response = llm_with_tools.invoke([
    user_message,
    response,
    tool_message
])

#final Answer
print(final_response.content)