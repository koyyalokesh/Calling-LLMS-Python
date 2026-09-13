
from pydantic import BaseModel, Field

from typing import Literal

from langchain_core.tools import tool


class ConvertInput(BaseModel):
    """input for the currency converter"""
    
    amount : float = Field(description="How many rupees to convert", gt=0)
    currency : Literal["USD","EUR","GBP"] = Field(description="currency to convert into")
    

@tool("convert_from_rupees", args_schema=ConvertInput)
def convert_from_rupees(amount:float, currency:str)->float:
    """Convert an Indian rupees into another currency."""
    rates = {"USD": 0.011, "EUR": 0.011, "GBP": 0.0094}
    return f"{amount} is about {amount*rates[currency]:.2f} {currency}"


print(convert_from_rupees.args)
print(convert_from_rupees.invoke({
    "amount":1000,
    "currency":"USD"
}))
    