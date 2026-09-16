from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms with world limit 30 words."
)

user_input = input()

message = prompt.invoke({"topic":user_input})

response = llm.invoke(message)

print(response.content)