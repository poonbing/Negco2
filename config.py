import os


class Config:
    # Flask configuration
    DEBUG = True  # Set to False in production
    SECRET_KEY = "your_secret_key"

    # xCaptcha configuration
    XCAPTCHA_SITE_KEY = "906a1dab-2e2c-4c80-880a-9fb359a89b73"
    XCAPTCHA_SECRET_KEY = "0xF9Eb4ffE0304E994f169619C85a0cbe3ca803D9B"
    XCAPTCHA_VERIFY_URL = "https://hcaptcha.com/siteverify"
    XCAPTCHA_API_URL = "https://hcaptcha.com/1/api.js"
    XCAPTCHA_DIV_CLASS = "h-captcha"

    # Database configuration
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:1817postgres%40pg@localhost:5432/users"
    )

    # Flask-Mail configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "chuayoushen5@gmail.com"
    MAIL_PASSWORD = "bqpccxputtnresrf"
    MAIL_DEFAULT_SENDER = ("NEGCO2", "chuayoushen@gmail.com")

    # Path Configuration
    APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "app"))
    STATIC_FOLDER = os.path.join(APP_ROOT, "static")
    UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, "images")
