from fastapi import HTTPException

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from models import create_all_tables
from view import OrderView, UserView
from interface import DataBaseInterface

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    create_all_tables()
    yield

app = FastAPI(
    title="Freelance exchange",
    version="1.0.0",
    lifespan=app_lifespan
)

@app.get("/")
def root():
    return "ok"


@app.post("/new_user")
def create_item(body: UserView):
    """данная функция создаёт пользователя"""
    new_user_id = DataBaseInterface.create_user(body)
    return {"user_id": new_user_id}


@app.post("/neworder")
def create_order(body: OrderView):
    """данная функция создаёт заказ"""
    new_order_id = DataBaseInterface.create_order(body)
    return {"order_id": new_order_id}


@app.get("/order/{_id}")
def get_order_id(_id: int):
    """Показать Заказ по его ID"""
    order = DataBaseInterface.get_order_by_id(_id)
    if order:
        return order_to_json(order)
    else:
        raise HTTPException(status_code=404, detail="Заказ не найден")


def order_to_json(order):
    return {
        "id": order.id,
        "executorId": order.executorId,
        "customerId": order.customerId,
        "theme": order.theme,
        "Price": order.Price,
        "URLPhoto": order.URLPhoto
        }


@app.get("/user/{_id}")
def get_user_id(_id: int):
    """Показать пользователя по его ID"""
    user = DataBaseInterface.get_user_by_id(_id)
    if user:
        return user_to_json(user)
    else:
        raise HTTPException(status_code=404, detail="Пользователь не найден")


def user_to_json(user):
    return {
        "id": user.id,
        "name": user.name,
        "portfolio": user.portfolio,
        "balance": user.balance
        }

@app.get("/all/users")
def get_all_users():
    """Показать всех пользователей"""
    users = DataBaseInterface.get_all_users()
    users_json = [user_to_json(user) for user in users]
    return users_json


@app.get("/all/orders")
def get_all_order():
    """Показать все заказы"""
    orders = DataBaseInterface.get_all_orders()
    orders_json = [order_to_json(order) for order in orders]
    return orders_json


@app.delete("/orderdel/{_id}")
def order_delete(_id: int):
    """Удаление заказа по его ID"""
    deleted = DataBaseInterface.delete_order_by_id(_id)
    if deleted:
        print("Заказ успешно удален вместе с его изображениями")
    else:
        print("Заказ с указанным идентификатором не найден")


@app.delete("/userdel/{_id}")
def user_delete(_id: int):
    """Удаление пользователя по его ID"""
    deleted = DataBaseInterface.delete_user_by_id(_id)
    if deleted:
        print("Пользователь успешно удален")
    else:
        print("Пользователь с указанным идентификатором не найден")


@app.put("/addorderPhoto/{order_id}")
def add_order_Photo(order_id: int, URLPhoto: str):
    """Добовать фото для заказа"""
    if not DataBaseInterface.update_order_URLPhoto(order_id, URLPhoto):
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return {"return": "Ссылка успешно обновлена"}


@app.put("/newaddorderPhoto/{order_id}")
def new_add_order_Photo(order_id: int, URLPhoto: str):
    """Добавленее фото к заказу с удалеение всех предыдуших фотографий"""
    if not DataBaseInterface.nupdate_order_URLPhoto(order_id, URLPhoto):
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return {"return": "Ссылка успешно обновлена"}


@app.put("/addorderexecutor/{order_id}")
def add_order_executor(order_id: int, executorId: int):
    """Добавить исполнителя к заказу"""
    if not DataBaseInterface.update_order_executor(order_id, executorId):
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return {"return": "Исполнитель успешно обновлён"}


@app.put("/newuserportfolio/{user_id}")
def new_update_user_portfolio(user_id: int, portfolio: str):
    """Добавить фото в портфолио пользователя"""
    if not DataBaseInterface.new_update_user_portfolio(user_id, portfolio):
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {"message": "Портфолио успешно обновлено"}

@app.put("/userportfolio/{user_id}")
def update_user_portfolio(user_id: int, portfolio: str):
    """Добавить фото в портфолио пользователя с удалением всех предыдущих фотографий"""
    if not DataBaseInterface.update_user_portfolio(user_id, portfolio):
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {"message": "Портфолио успешно обновлено"}


@app.put("/confirm_order/{order_id}")
def confirm_order(order_id: int):
    """Поодтверждение заказа и переход средств, а также удаление заказа"""
    if not DataBaseInterface.confirm_order(order_id):
        pass
    return {"message": "Заказ успешно подтвержден и средства успешно списаны и зачислены"}




if __name__ == "__main__":
    uvicorn.run(app)

