from sqlalchemy import select

from connector import session_factory
from view import UserView, PicturView, OrderView, OrederPicturView
from models import User, Orders

class DataBaseInterface:


    @classmethod
    def create_order(cls, order: OrderView):
        with session_factory() as session:
            order = Orders(
                theme=order.theme,
                Price=order.Price,
                userid=order.userid
            )
            session.add(order)
            session.flush()
            session.commit()
            _id = order.id
            return _id


    @classmethod
    def get_item_by_id(cls, _id: int):
        with session_factory() as session:
            order = select(Orders).where(Orders.id == _id)
            order = session.execute(order)
            print(order)
            order = order.unique().scalars().all()
            print(order)
            return order[0]