from pydantic import BaseModel, field_validator
from enum import IntEnum
from datetime import datetime

'''
This module serves as the base of this project by defining essential 
components through Pydantic models. 

Each class is build to encapsulate specific validation rules, constraints,
and error-handling mechanisms tailored to its purpose.

Key Features:
- Comprehensive Validation: Ensures data integrity and correctness through Pydantic's robust validation system.
- Custom Constraints: Tailored constraints are applied to each class, maintaining consistency and enforcing project-specific standards.
- Error Handling: Robust error-handling mechanisms are embedded in each class, providing clear and informative feedback in case of data discrepancies.

Usage Guidelines:
- Reference these Pydantic models when building methods throughout the project to leverage consistent validation behavior.
- Eliminate Code Duplication: By adhering to the predefined validation standards in these classes, code duplication is minimized, 
    fostering maintainability and coherence.
'''

class Price(BaseModel):
    # accepts float None and zero
    price: float | None

    @field_validator('price',mode='after')
    def validate_price(cls, value):
        ## Uncomment the following lines will enable None types for price
        # if value == None:
            # return value
        if not isinstance(value, float):
            raise ValueError("Price must be a numeric value, not a string")

        if value < 0:
            raise ValueError("Price must be greater than 0")

        return value

class DividendAmount(BaseModel):
    # Accepts float none and zero
    dividend_amount: float | None

    @field_validator("dividend_amount", mode="after")
    def validate_dividend(cls, value):
        if value == None:
            value = 0.0
        if not isinstance(value, float):
            raise ValueError("Dividend must be numeric")
        
        if value < 0:
            raise ValueError("Dividend cannot be negative")
        return value

class DividendPct(BaseModel):
    # Accepts float none and zero and str with % symbol
    dividend_pct: float | None

    @field_validator("dividend_pct", mode="before")
    def validate_dividend_str(cls, value):
        if isinstance(value, str):
            stripped_value = value.strip()
            replaced_value = stripped_value.replace(" ", "").replace("%", "")
            value = replaced_value
        return value

    @field_validator("dividend_pct", mode="after")
    def validate_dividend(cls, value):
        if value == None:
            return 0.0
        if not isinstance(value, float):
            raise ValueError("Dividend must be numeric")
        
        if value < 0:
            raise ValueError("Dividend cannot be negative")
        return value

class Quantity(BaseModel):
    # Accepts only positing numbers. But supports floating for case of fractional shares
    quantity: float | None

    @field_validator('quantity', mode='after')
    def validate_quantity(cls, value):
        if not isinstance(value, float):
            raise ValueError("Quantity must be numeric")
        
        if value <= 0:
            raise ValueError("Quantity cannot be negative or possitive")
        return value

class ParValue(BaseModel):
    par_value: float | None

    
    @field_validator('par_value', mode='after')
    def validate_par_value(cls, value):
        if not isinstance(value, float):
            raise ValueError("Quantity must be numeric")
        
        if value <= 0:
            raise ValueError("Quantity cannot be negative or possitive")
        return value

class OrderType(IntEnum):
    BUY = 1
    SELL = 0

class Order(BaseModel):
    order: OrderType

    @field_validator("order", mode="before")
    def validate_order(cls, value):
        if isinstance(value, str):
            if value.upper() in OrderType.__members__.keys():
                order_value = value.upper()
                return OrderType[order_value].value
            else:
                raise ValueError("Order type can only be", OrderType.__members__.keys())
        return value
    
    @property
    def order_type(self):
        return self.order.value
    
    @property
    def order_name(self):
        return self.order.name

class Trade(Price, Quantity, Order):
    timestamp: datetime

    @field_validator("timestamp", mode="before")
    def parse_timestamp(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except Exception as e:
            raise ValueError("Timestamp format is not correct for", value)
    @property
    def trade(self):
        return {
            "price":self.price, 
            "timestamp":self.timestamp.strftime("%Y-%m-%d %H:%M:%S"), 
            "quantity":self.quantity, 
            "order":self.order_name
            }

