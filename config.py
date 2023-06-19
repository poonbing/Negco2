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

    # Other application settings
    STATIC_URL_PATH = "/static"
    STATIC_FOLDER = "static"
