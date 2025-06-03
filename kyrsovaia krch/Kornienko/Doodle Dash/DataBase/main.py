import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from uvicorn import lifespan

from models import create_all_tables
from view import OrderView
from interface import DataBaseInterface


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all_tables()
    yield


app = FastAPI(
    title="Freelance exchange",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
def root():
    return "ok"

@app.post("/neworder")
def create_order(body: OrderView):
    new_order_id = DataBaseInterface.create_order(body)
    return {"order_id": new_order_id}


@app.get(path="/item/{_id}")
def get_item(_id: int):
    order = DataBaseInterface.get_item_by_id(_id)
    return OrderView.model_validate(order, from_attributes=True)


if __name__ == "__main__":
    uvicorn.run(app)