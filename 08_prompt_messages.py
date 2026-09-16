from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a {language} trainer. Keep answers under {limit} words"
        
    ),
    (
        "human",
        "Explain {topic} to a beginner"
    )
])


filled = prompt.invoke(
    {
        "language" : "Python",
        "limit" : 30,
        "topic" : "decorators"
    }
)


response = llm.invoke(filled)

print(type(response))
print(response.content)