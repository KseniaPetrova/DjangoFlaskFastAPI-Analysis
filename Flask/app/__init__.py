from flask import Flask
from flask_session import Session  # Для работы с сессиями
from .routes import main as main_blueprint


def create_app() -> Flask:
    """Создает и конфигурирует экземпляр приложения Flask.

    Returns:
        Flask: Настроенный экземпляр Flask приложения.
    """
    app: Flask = Flask(__name__, template_folder='templates')

    # Конфигурация для сессий
    app.config['SECRET_KEY'] = 'secret_key'  # Секретный ключ для подписи сессий
    app.config['SESSION_TYPE'] = 'filesystem'  # Тип сессии, использующий файловую систему
    Session(app)  # Инициализация сессии

    # Регистрация синихprints
    app.register_blueprint(main_blueprint)

    return app