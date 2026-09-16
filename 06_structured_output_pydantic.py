from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

load_dotenv()

class Product(BaseModel):
    name : str
    price : int
    category : str
    
llm = ChatOpenAI(model="gpt-4o-mini")

structured_llm = llm.with_structured_output(Product)


message = """"The new iPhone 16 is available for $799.
It comes with an A18 chip."""

response = structured_llm.invoke(message)

print(response)

print(response.name)
print(response.price)
print(response.category)

