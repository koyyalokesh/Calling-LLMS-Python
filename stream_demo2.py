from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = ChatPromptTemplate.from_messages([("human","Explain {topic} in simple terms within 80 word limit")])

llm = ChatOpenAI(model="gpt-4o-mini")

chain = prompt | llm | StrOutputParser()

for chunk in chain.stream({"topic":"Oops"}):
    print(chunk, end="", flush=True)
    
    