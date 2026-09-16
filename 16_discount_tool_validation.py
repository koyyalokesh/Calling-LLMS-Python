from pydantic import BaseModel, Field

from langchain_core.tools import tool

class DiscountInput(BaseModel):
    price:float = Field(...,gt=0)
    discount:float = Field(..., gt=0,le=100)
    
@tool("calculate_discount", args_schema=DiscountInput)
def calculate_discount(price:float, discount:float)->float:
    """Calculate the final price after applying a percentage discount."""
    discount_amount = price*(discount/100)
    final_price = price - discount_amount
    return final_price



result = calculate_discount.invoke({
    "price":1000,
    "discount":2
})

print(result);