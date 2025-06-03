from pydantic import BaseModel

class UserView(BaseModel):
    id: int
    name: str
    password: str


class PicturView(BaseModel):
    id: int
    file: str
    userId: int

class OrderView(BaseModel):
    id: int
    theme: str
    userid: int
    Price: float

class OrederPicturView(BaseModel):
    id: int
    OrderId: int
    Pictur: str


