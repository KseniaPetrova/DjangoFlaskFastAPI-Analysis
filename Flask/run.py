from app import create_app
from app.db import engine, Base
from flask import Flask

app: Flask = create_app()  # Создаем экземпляр приложения Flask


def create_tables() -> None:
    """Создает все таблицы в базе данных, используя метаданные ORM."""
    with app.app_context():
        Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()  # Создание таблиц перед запуском приложения
    app.run(debug=True)  # Запускаем приложение в режиме отладки

# python run.py