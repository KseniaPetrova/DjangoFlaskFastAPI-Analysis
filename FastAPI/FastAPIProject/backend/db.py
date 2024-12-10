from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from typing import Generator

# Создание двигательного механизма базы данных
engine = create_engine('sqlite:///db_users.db', echo=True)

SessionLocal = sessionmaker(bind=engine)

# Базовый класс для моделей
class Base(DeclarativeBase):
    pass

async def get_db() -> Generator[SessionLocal, None, None]:
    """Асинхронно получает сеанс базы данных.

    Используется как контекстный менеджер для работы с сессиями
    в запросах. Закрывает сеанс после завершения работы.

    Yields:
        SessionLocal: Сессия базы данных для выполнения операций.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Закрываем сеанс после использования
