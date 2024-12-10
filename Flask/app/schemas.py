from dataclasses import dataclass
from typing import Optional


# Базовая модель пользователя
@dataclass
class UserBase:
    """Базовая модель пользователя, содержащая общие атрибуты.

    Attributes:
        username (str): Уникальное имя пользователя.
        email (str): Уникальный адрес электронной почты.
        phone_number (str): Номер телефона пользователя.
    """
    username: str
    email: str
    phone_number: Optional[str]  # phone_number может быть пустым


# Модель пользователя при регистрации
@dataclass
class UserCreate(UserBase):
    """Модель пользователя для регистрации, включает пароль и его подтверждение.

    Attributes:
        password (str): Пароль пользователя.
        password_confirmation (str): Подтверждение пароля.
    """
    password: str
    password_confirmation: str


# Модель пользователя для логина
@dataclass
class UserLogin:
    """Модель пользователя для логина.

    Attributes:
        username (str): Уникальное имя пользователя.
        password (str): Пароль пользователя.
    """
    username: str
    password: str


# Полная модель пользователя для представления
@dataclass
class User(UserBase):
    """Полная модель пользователя, включая идентификатор и захешированный пароль.

    Attributes:
        id (int): Уникальный идентификатор пользователя.
        hashed_password (str): Захешированный пароль пользователя для хранения.
    """
    id: int
    hashed_password: str