import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base Configuration"""
    SECRET_KEY = os.getenv("SECRET_KEY", "watch-store-secret-key-default-2026")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/watch_store")
    USE_MONGOMOCK = os.getenv("USE_MONGOMOCK", "False").lower() in ("true", "1", "yes")

    # Mail Configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() in ("true", "1", "yes")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() in ("true", "1", "yes")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", None)
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", None)
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "WatchStore <no-reply@watchstore.com>")

    # Pagination
    ITEMS_PER_PAGE = 8

    # Network / External APIs
    EXCHANGE_RATE_API_URL = os.getenv("EXCHANGE_RATE_API_URL", "https://open.er-api.com/v6/latest/USD")
    VIETQR_API_URL = os.getenv("VIETQR_API_URL", "https://api.vietqr.io/v2/banks")


class DevelopmentConfig(Config):
    """Development Configuration"""
    DEBUG = True


class TestingConfig(Config):
    """Testing Configuration"""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    USE_MONGOMOCK = True
    MONGO_URI = "mongodb://localhost:27017/watch_store_test"


class ProductionConfig(Config):
    """Production Configuration"""
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}

