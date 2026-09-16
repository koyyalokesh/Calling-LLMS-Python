from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

@tool
def book_seat(name:str,seat:str)->str:
    """Book a seat in the class for a person."""
    return f"Seat {seat} booked for {name}."

llm = ChatOpenAI(model="gpt-4o-mini")

agent = create_agent(
    model=llm,
    tools=[book_seat],
    system_prompt="You help learners book a seat in the langchain class.",
    checkpointer=InMemorySaver() #tells the agent to store the conversation after each step
)


def ask(question, thread_id):
    result=agent.invoke(
        {
            "messages":[{"role":"user", "content":question}]
        },
        config={"configurable":{"thread_id":thread_id}},
    )
    print(f"[{thread_id}] Q: {question}")
    print(f"[{thread_id}] A: {result['messages'][-1].content}")
    
    

ask("My name is vinay kumar gurram", thread_id="vinay")
ask("Book me a seat A12.", thread_id="nimish")
ask("What is my name and what seat did i book", thread_id="vinay")
ask("What is my name and what seat did i book", thread_id="nimish")