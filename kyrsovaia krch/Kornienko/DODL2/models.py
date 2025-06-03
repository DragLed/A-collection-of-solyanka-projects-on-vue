from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Annotated
from sqlalchemy import BigInteger, ForeignKey, Column, String

from connector import engine

intpk = Annotated[int, mapped_column(BigInteger, primary_key=True)]



class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]
    portfolio: Mapped[str]
    balance: Mapped[float]


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[intpk] = mapped_column(primary_key=True)
    theme: Mapped[str]
    customerId: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    executorId: Mapped[int]
    Price: Mapped[float]
    URLPhoto: Mapped[str]
    confirmed: Mapped[bool]


def create_all_tables():
    Base.metadata.create_all(bind=engine)







