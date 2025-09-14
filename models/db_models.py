from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from db.session import Base

class ClientORM(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    phone: Mapped[str] = mapped_column(String(32))
    age: Mapped[int] = mapped_column(Integer)
