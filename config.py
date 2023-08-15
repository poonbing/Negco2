import os
import logging
import secrets, os


class Config:
    # Security configuration
    DEBUG = True
    SECRET_KEY = "pf9Wlove4IKEAXvy-cQkeDPhv9Az3Ay-zqGILbp_ySc"
    ENCRYPTION_KEY = b"hRqDT_oQOosfS5GZHd8-C7hfo4jClUyn7kdZT-HBt6I="
    key = secrets.token_urlsafe(16)
    SECRET_KEY = key
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 1800

    # xCaptcha configuration
    XCAPTCHA_SITE_KEY = "906a1dab-2e2c-4c80-880a-9fb359a89b73"
    XCAPTCHA_SECRET_KEY = "0xF9Eb4ffE0304E994f169619C85a0cbe3ca803D9B"
    XCAPTCHA_VERIFY_URL = "https://hcaptcha.com/siteverify"
    XCAPTCHA_API_URL = "https://hcaptcha.com/1/api.js"
    XCAPTCHA_DIV_CLASS = "h-captcha"

    # Database configuration
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://Negco_Admin:Forehead_Gang@it2555.mysql.database.azure.com/neggo2"

    # Flask-Mail configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "negco2lewis@gmail.com"
    MAIL_PASSWORD = "beshzazmbzfokmig"
    MAIL_DEFAULT_SENDER = ("NEGCO2", "negco2lewis@gmail.com")

    # Path Configuration
    APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "app"))
    STATIC_FOLDER = os.path.join(APP_ROOT, "static")
    UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, "images")

    # Oauth Configuration
    GOOGLE_CLIENT_ID = (
        "43510388979-2l3aedm3mce7trakvl09n9rcblcm1lco.apps.googleusercontent.com"
    )
    GOOGLE_CLIENT_SECRET = "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"
    AZURE_CLIENT_ID = "2853d287-14c5-45dd-97f7-89d9bd06f37c"
    AZURE_CLIENT_SECRET = "8304bf93-0a20-459d-89a9-0fff0b169e0f"

    # Logging Configuration
    LOG_FILE = "record.log"
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
