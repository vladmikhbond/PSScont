from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class Problem(Base):
    __tablename__ = "problems"
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    attr: Mapped[str] = mapped_column(String(255))
    lang: Mapped[str] = mapped_column(String(5))
    cond: Mapped[str] = mapped_column(String)
    view: Mapped[str] = mapped_column(String)
    hint: Mapped[str] = mapped_column(String)
    code: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String(10))  
    timestamp: Mapped[str] = mapped_column(DateTime)


class User(Base):
    """ password hashed
        role (1 student, 2 tutor, 4 admin) 
    """
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column(String(255))
    role: Mapped[int] = mapped_column(Integer)