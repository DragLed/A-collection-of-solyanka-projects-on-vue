from fastapi import HTTPException
from sqlalchemy import select, delete
from connector import session_factory
from view import OrderView, UserView
from models import Orders, User


class DataBaseInterface:

    @classmethod
    def create_order(cls, order: OrderView):
        with session_factory() as session:
            order_db = Orders(
                theme=order.theme,
                customerId=order.customerId,
                executorId=order.executorId,
                Price=order.Price,
                URLPhoto=order.URLPhoto,
                confirmed=False
            )
            session.add(order_db)
            session.flush()
            session.commit()
            _id = order_db.id
            return _id


    @classmethod
    def create_user(cls, user: UserView):
        with session_factory() as session:
            user_db = User(
                name=user.name,
                password=user.password,
                balance=user.balance,
                portfolio="NONE"
            )
            session.add(user_db)
            session.flush()
            session.commit()
            _id = user_db.id
            return _id

    @classmethod
    def get_order_by_id(cls, _id: int):
        with session_factory() as session:
            order = select(Orders).where(Orders.id == _id)
            order = session.execute(order)
            order = order.unique().scalars().first()
            return order

    @classmethod
    def get_order_by_theme(cls, theme: str):
        with session_factory() as session:
            order1 = select(Orders).where(Orders.theme == theme)
            order1 = session.execute(order1)
            order1 = order1.unique().scalars().first()
            return order1
    @classmethod
    def get_all_orders(cls):
        with session_factory() as session:
            orders = session.query(Orders).all()
            return orders

    @classmethod
    def get_user_by_id(cls, _id: int):
        with session_factory() as session:
            user = select(User).where(User.id == _id)
            user = session.execute(user)
            user = user.unique().scalars().first()
            return user

    @classmethod
    def get_all_users(cls):
        with session_factory() as session:
            users = session.query(User).all()
            return users


    @classmethod
    def delete_order_by_id(cls, _id: int):
        with session_factory() as session:
            order = delete(Orders).where(Orders.id == _id)
            result = session.execute(order)
            session.commit()
            return result.rowcount > 0

    @classmethod
    def delete_user_by_id(cls, _id: int):
        with session_factory() as session:
            user = delete(User).where(User.id == _id)
            result = session.execute(user)
            session.commit()
            return result.rowcount > 0

    @classmethod
    def nupdate_order_URLPhoto(cls, order_id: int, URLPhoto: str):
        with session_factory() as session:
            order = session.query(Orders).filter(Orders.id == order_id).first()
            if order:
                order.URLPhoto = URLPhoto
                session.commit()
                return True
            return False

    @classmethod
    def update_order_URLPhoto(cls, order_id: int, URLPhoto: str):
        with session_factory() as session:
            order = session.query(Orders).filter(Orders.id == order_id).first()
            if order:
                if order.URLPhoto:
                    order.URLPhoto = f"{order.URLPhoto}, {URLPhoto}"
                else:
                    order.URLPhoto = URLPhoto
                session.commit()
                return True
            return False


    @classmethod
    def update_order_executor(cls, order_id: int, executorId: int):
        with session_factory() as session:
            order = session.query(Orders).filter(Orders.id == order_id).first()
            if order:
                order.executorId = executorId
                session.commit()
                return True
            return False


    @classmethod
    def update_user_portfolio(cls, user_id: int, new_portfolio_data: str):
        with session_factory() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                if user.portfolio:
                    user.portfolio += ",  " + new_portfolio_data
                else:
                    user.portfolio = new_portfolio_data
                session.commit()
                return True
            return False

    @classmethod
    def new_update_user_portfolio(cls, user_id: int, portfolio: str):
        with session_factory() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                user.portfolio = portfolio
                session.commit()
                return True
            return False

    @classmethod
    def confirm_order(cls, order_id: int):
        with session_factory() as session:
            order = session.query(Orders).filter(Orders.id == order_id).first()
            if order:
                customer = session.query(User).filter(User.id == order.customerId).first()
                executor = session.query(User).filter(User.id == order.executorId).first()
                if customer.balance >= order.Price:
                    customer.balance -= order.Price
                    executor.balance += order.Price
                    order.confirmed = True
                    order = delete(Orders).where(Orders.id == order_id)
                    result = session.execute(order)
                    session.commit()

                    return True, result.rowcount > 0
                else:
                    raise HTTPException(status_code=400, detail="Недостаточно средств на балансе заказчика")
            else:
                raise HTTPException(status_code=404, detail="Заказ не найден")