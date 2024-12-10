from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
from typing import Generator

# Создание движка базы данных
DATABASE_URL = 'sqlite:///db_users.db'
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


@contextmanager
def get_db() -> Generator[SessionLocal, None, None]:
    """Создает и управляет сессией базы данных.

    Используется как контекстный менеджер. Позволяет получить сессию
    для выполнения операций над базой данных. В случае ошибки
    будет выполнен откат изменений.

    Yields:
        SessionLocal: Сессия для работы с базой данных.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()  # Коммит изменений только если не было исключений
    except Exception:
        db.rollback()  # Откатить изменения в случае ошибки
        raise  # Повторно выбрасываем исключение
    finally:
        db.close()  # Закрываем сессию
