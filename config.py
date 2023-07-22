import os


class Config:
    # Security configuration
    DEBUG = True
    SECRET_KEY = "pf9Wlove4IKEAXvy-cQkeDPhv9Az3Ay-zqGILbp_ySc"
    SECURITY_PASSWORD_SALT = "146585145368522386173505678016728509634"

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
    MAIL_USERNAME = "chuayoushen5@gmail.com"
    MAIL_PASSWORD = "bqpccxputtnresrf"
    MAIL_DEFAULT_SENDER = ("NEGCO2", "chuayoushen@gmail.com")

    # Path Configuration
    APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "app"))
    STATIC_FOLDER = os.path.join(APP_ROOT, "static")
    UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, "images")

    # Talisman Configuration
    TALISMAN_FORCE_HTTPS = True
    TALISMAN_SESSION_COOKIE_SECURE = True
    TALISMAN_CONTENT_SECURITY_POLICY = {
        "default-src": [
            "'self'",
            "cdnjs.cloudflare.com",
        ],
        "script-src": [
            "'self'",
            "cdnjs.cloudflare.com",
        ],
        "img-src": [
            "'self'",
            "data:",
        ],
    }
