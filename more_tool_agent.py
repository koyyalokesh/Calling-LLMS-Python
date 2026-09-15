#Four tools, and letting the agent choose

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


#order database
ORDERS = {
    "ORD-1001":{"item":"Wireless mouse", "status":"shipped","amount":1499},
    "ORD-1002":{"item":"Mechanical Keyboard", "status":"packed", "amount":4999},
}

#warehouse stock database
STOCK={"wireless mouse":12, "mechanical keyboard":0, "usb hub":34}


@tool
def order_status(order_id:str)->str:
    """Get the status and amount of an order using its id, for example ORD-1001."""
    order = ORDERS.get(order_id.upper())
    if order is None:
        return f"No order found with id {order_id}."
    return f"{order['item']}, status {order['status']}, amount{order['amount']} rupees"

@tool
def check_stock(item:str)->str:
    """Check how many units of an item are left in the warehouse."""
    count = STOCK.get(item.lower())
    if count is None :
        return f"{item} is not in catalogue."
    return f"{count} units of {item} in stock"

@tool
def apply_discount(amount:float, percent:float)->float:
    """Apply a discount percentage to an amount and return the new amount."""
    return round(amount - (amount * percent / 100), 2)


@tool
def delivery_days(pin_code:str)->str:
    """Estimate delivery time for an Indian pin code."""
    metro ={"530048", "530049", "530050"}
    return "2 days" if pin_code in metro else "5 days"



agent = create_agent(
    model=llm,
    tools=[order_status, check_stock, apply_discount, delivery_days],
    system_prompt=(
        "You are a support assistant for an online store. "
        "Use the tools for anything about orders, stock, pricing or delivery. "
        "Never guess a number, look it up."
    )
)


def ask(question):
    print("Q:", question)
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    print("A:", result["messages"][-1].content)
    print("-" * 60)

ask("For ORD-1002, what would the price be after a 10 percent discount.")