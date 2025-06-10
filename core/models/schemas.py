from sqlalchemy.orm import DeclarativeBase,mapped_column,Mapped,relationship
from sqlalchemy import Integer, String,ForeignKey


class Base(DeclarativeBase):
    __abstract__ = True
    id:Mapped[int] = mapped_column(primary_key=True)




class Client(Base):

    __tablename__ = "Clients"

    name:Mapped[str]
    surname:Mapped[str]
    email:Mapped[str]
    age:Mapped[int]


class User(Base):

    __tablename__ = "Users"

    username:Mapped[str] = mapped_column(String(50),unique=True)
    password:Mapped[str]
    email:Mapped[str] = mapped_column(String(80))