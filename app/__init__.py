# Python Modules
from flask import Flask
from flask_xcaptcha import XCaptcha

# Local Modules
from config import Config
from .extensions import db, mail, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    xcaptcha = XCaptcha(app=app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from app.main import bp as main_bp
    from app.login import bp as login_bp
    from app.user import bp as user_bp
    from app.admin import bp as admin_bp
    from app.password_recovery import bp as password_recovery_bp
    from app.error import bp as error_bp
    from app.signup import bp as signup_bp
    from app.api import bp as api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(password_recovery_bp)
    app.register_blueprint(error_bp)
    app.register_blueprint(api_bp)

    login_bp.xcaptcha = xcaptcha

    return app
