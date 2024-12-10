from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import User
from .db import get_db
from passlib.context import CryptContext
from flask import Response

main = Blueprint('main', __name__)
pwd_context = CryptContext(schemes=["scrypt"])


@main.route("/", methods=["GET"])
def menu() -> Response:
    """Отображает главную страницу меню.

    Returns:
        Response: HTML-шаблон для отображения меню.
    """
    user_authenticated = session.get("user_authenticated", False)
    return render_template("menu.html", user_authenticated=user_authenticated)


@main.route("/register", methods=["GET", "POST"])
def register() -> Response:
    """Обрабатывает регистрацию нового пользователя.

    Returns:
        Response: HTML-шаблон для отображения формы регистрации или перенаправление после успешной регистрации.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_confirmation = request.form["password_confirmation"]
        email = request.form["email"]
        phone_number = request.form.get("phone_number")

        # Проверка на совпадение паролей
        if password != password_confirmation:
            return render_template("register.html", error="Пароли не совпадают.")

        # Подключение к базе данных с использованием контекста
        with get_db() as db:
            db_user = db.query(User).filter(User.username == username).first()
            if db_user:
                return render_template("register.html", error="Пользователь уже зарегистрирован.")

            hashed_password = pwd_context.hash(password)
            new_user = User(username=username, email=email, password=hashed_password, phone_number=phone_number)

            db.add(new_user)
            db.commit()  # Коммитим изменения

        session["user_authenticated"] = True
        session["username"] = username

        return redirect(url_for('main.homenotes'))

    return render_template("register.html", error=None)


@main.route("/login", methods=["GET", "POST"])
def login() -> Response:
    """Обрабатывает процесс входа пользователя.

    Returns:
        Response: HTML-шаблон для отображения формы входа или перенаправление после успешного входа.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            # Подключение к базе данных с использованием контекста
            with get_db() as db:
                user = db.query(User).filter(User.username == username).first()

                # Проверка пользователя
                if not user or not pwd_context.verify(password, user.password):
                    return render_template("login.html", error="Неправильное имя пользователя или пароль.")

                session["user_authenticated"] = True
                session["username"] = user.username

                return redirect(url_for('main.homenotes'))
        except Exception as e:
            # Логирование ошибки или обработка
            return render_template("login.html", error="Произошла ошибка при входе.")

    return render_template("login.html")


@main.route("/homenotes", methods=["GET"])
def homenotes() -> Response:
    """Отображает страницу заметок пользователя.

    Returns:
        Response: HTML-шаблон для отображения заметок.
    """
    return render_template("homenotes.html")


@main.route("/logout", methods=["POST"])
def logout() -> Response:
    """Выход пользователя из системы.

    Returns:

    Response: Перенаправление на главную страницу меню.
"""
    session.clear()  # Очищаем сессию
    return redirect(url_for('main.menu'))
