from typing import Optional

from pydantic import BaseModel

class UserView(BaseModel):
    id: int
    name: str
    password: str
    portfolio: Optional[str] = None
    balance: float = 0.0


class OrderView(BaseModel):
    id: int
    theme: str
    customerId: int
    executorId: Optional[int] = None
    Price: float
    URLPhoto: Optional[str] = None
    confirmed: bool = False



