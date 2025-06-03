from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Annotated
from sqlalchemy import BigInteger,  ForeignKey


from connector import engine

intpk = Annotated[int, mapped_column(BigInteger, primary_key=True)]



class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[intpk] = mapped_column(primary_key=True)
    userid: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    theme: Mapped[str]
    Price: Mapped[int]


class OrederPicturView(Base):
    __tablename__ = "OrederPicturs"

    id: Mapped[intpk] = mapped_column(primary_key=True)
    OrederId: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    Pictur: Mapped[str]


def create_all_tables():
    Base.metadata.create_all(bind=engine)







