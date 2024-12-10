from pydantic import BaseModel, EmailStr, constr

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=30)  # Ограничение длины имени пользователя
    email: EmailStr  # Используем валидатор для Email
    phone_number: constr(min_length=10, max_length=15)  # Ограничение длины номера телефона

class UserCreate(UserBase):
    password: constr(min_length=8)  # Минимальная длина пароля
    password_confirmation: str

    @classmethod
    async def from_form(cls, form) -> "UserCreate":
        """Создает экземпляр UserCreate из данных формы.

        Args:
            form (dict): Данные, полученные из формы.

        Returns:
            UserCreate: Экземпляр модели UserCreate.
        """
        return cls(
            username=form.get("username"),
            email=form.get("email"),
            phone_number=form.get("phone_number"),
            password=form.get("password"),
            password_confirmation=form.get("password_confirmation"),
        )

class UserLogin(BaseModel):
    username: str  # Имя пользователя
    password: str  # Пароль

class User(UserBase):
    """Схема для пользователя с дополнительными полями."""

    id: int  # Уникальный идентификатор пользователя
    hashed_password: str  # Захешированный пароль

    class Config:
        orm_mode = True  # Позволяет использовать объекты ORM с этой схемой












