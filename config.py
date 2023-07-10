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
        'mysql+mysqlconnector://Negco_Admin:Forehead_Gang@it2555.mysql.database.azure.com/neggo2'
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

    # SSO provider configuration
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    MICROSOFT_CLIENT_ID = os.environ.get("MICROSOFT_CLIENT_ID")
    MICROSOFT_CLIENT_SECRET = os.environ.get("MICROSOFT_CLIENT_SECRET")
    GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")