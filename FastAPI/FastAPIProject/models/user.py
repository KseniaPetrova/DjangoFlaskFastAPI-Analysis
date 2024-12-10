from backend.db import Base
from sqlalchemy import Column, Integer, String
from typing import Optional

class User(Base):
    """Модель пользователя для базы данных.

    Атрибуты:
        id (int): Уникальный идентификатор пользователя.
        username (str): Уникальное имя пользователя.
        email (str): Уникальный адрес электронной почты пользователя.
        phone_number (Optional[str]): Номер телефона пользователя (может быть пустым).
        password (str): Захешированный пароль пользователя.
    """

    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, unique=True, index=True)
    email: str = Column(String, unique=True, index=True)
    phone_number: Optional[str] = Column(String, nullable=True)  # Сделаем параметр 'nullable=True' для явного указания
    password: str = Column(String)






