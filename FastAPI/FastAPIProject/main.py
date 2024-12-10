from fastapi import FastAPI, Request, Depends
from router import user
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.add_middleware(SessionMiddleware, secret_key="secret_key")

# Подключаем маршрутизатор пользователй
app.include_router(user.router)

@app.get("/")
async def menu(request: Request) -> templates.TemplateResponse:
    """Главное меню, проверяет состояние аутентификации пользователя.

    Args:
        request (Request): HTTP-запрос.

    Returns:
        TemplateResponse: Шаблон главного меню с информацией об аутентификации пользователя.
    """
    user_authenticated = request.session.get("user_authenticated", False)
    return templates.TemplateResponse("menu.html", {
        "request": request,
        "user_authenticated": user_authenticated
    })


@app.get("/register")
async def register(request: Request) -> templates.TemplateResponse:
    """Страница регистрации пользователя.

    Args:
        request (Request): HTTP-запрос.

    Returns:
        TemplateResponse: Шаблон страницы регистрации.
    """
    return templates.TemplateResponse("register.html", {
        "request": request,
        "error": None
    })


@app.get("/login")
async def login(request: Request) -> templates.TemplateResponse:
    """Страница входа пользователя.

    Args:
        request (Request): HTTP-запрос.

    Returns:
        TemplateResponse: Шаблон страницы входа.
    """
    return templates.TemplateResponse("login.html", {
        "request": request
    })


@app.get("/homenotes")
async def homenotes(request: Request) -> templates.TemplateResponse:
    """Страница заметок пользователя.

    Args:
        request (Request): HTTP-запрос.

    Returns:
        TemplateResponse: Шаблон страницы заметок.
    """
    return templates.TemplateResponse("homenotes.html", {
        "request": request
    })

