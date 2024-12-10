from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import Annotated
from schemas import UserCreate  # Убедитесь, что импортируете необходимые схемы
from models.user import User
from backend.db import get_db
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/users", tags=["users"])
pwd_context = CryptContext(schemes=["scrypt"])
templates = Jinja2Templates(directory='templates')


@router.post("/register")
async def create_user(db: Annotated[Session, Depends(get_db)], request: Request) -> RedirectResponse:
    """Регистрация нового пользователя.

    Подготавливает данные для регистрации пользователя, проверяет их на валидность и
    сохраняет нового пользователя в базе данных.

    Args:
        db (Session): Сессия базы данных.
        request (Request): HTTP-запрос.

    Returns:
        RedirectResponse: Перенаправление на страницу заметок при успешной регистрации
        или отрисовка шаблона регистрации с ошибкой.
    """
    form_data = await request.form()
    user = UserCreate.from_form(form_data)

    if user.password != user.password_confirmation:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Пароли не совпадают."
        })

    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Пользователь уже зарегистрирован."
        })

    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        phone_number=user.phone_number
    )

    request.session["user_authenticated"] = True
    request.session["username"] = user.username

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return RedirectResponse(url='/homenotes', status_code=303)


@router.post("/logout")
async def logout(request: Request) -> RedirectResponse:
    """Выход из системы.

    Удаляет данные сессии пользователя и перенаправляет его на главную страницу.

    Args:
        request (Request): HTTP-запрос.

    Returns:
        RedirectResponse: Перенаправление на главную страницу.
    """
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)) -> RedirectResponse:
    """Вход пользователя в систему.

    Проверяет имя пользователя и пароль, и если аутентификация проходит успешно,
    устанавливает сессию пользователя.

    Args:
        request (Request): HTTP-запрос.
        db (Session): Сессия базы данных.

    Returns:
        RedirectResponse: Перенаправление на страницу заметок при успешном входе
        или отрисовка шаблона входа с ошибкой.
    """
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")

    user = db.query(User).filter(User.username == username).first()

    if not user or not pwd_context.verify(password, user.password):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Неправильное имя пользователя или пароль."
        })

    request.session["user_authenticated"] = True
    request.session["username"] = user.username

    return RedirectResponse(url='/homenotes', status_code=303)
