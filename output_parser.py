from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser


load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

response = llm.invoke("Who is Mahindra Singh Dhoni")

print(response)

# 1. AIMessage in, plain string out

text_parser = StrOutputParser()

result = text_parser.invoke(response)

print(type(result))

print(result)

# 2. AIMessage in, python dictionary out

json_parser = JsonOutputParser()
json_prompt = ChatPromptTemplate.from_messages([
(
"system",
"Reply with JSON only, using the keys name, creator and year."
),
(
"human",
"Tell me about the {topic} framework."
),
])
filled = json_prompt.invoke({"topic": "Django"})
raw_reply = llm.invoke(filled)
data = json_parser.invoke(raw_reply)
"""print(type(data))
print(data["name"], "was created in", data["year"])"""

print(data)