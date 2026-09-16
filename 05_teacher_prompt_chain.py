from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful teacher.

    Explain {topic} to a {level} student.

    Give:
    1. Simple definition
    2. Real-world example
    word limit = 50

    """
)

chain = prompt | llm
response = chain.invoke({
    "topic":"ml",
    "level":"beginner"
})

print(response.content)