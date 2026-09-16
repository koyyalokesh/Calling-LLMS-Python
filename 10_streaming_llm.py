from dotenv import load_dotenv 

from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

# 1. streaming directly from the model
for chunk in llm.stream("who is mahindra singh dhoni."):
    print(chunk.content, end="", flush=True)