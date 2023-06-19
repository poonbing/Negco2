from flask import Flask
from flask_xcaptcha import XCaptcha

# Local Modules
from config import Config
from .extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    xcaptcha = XCaptcha(app=app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

        from app.main import bp as main_bp
        from app.login import bp as login_bp
        from app.user import bp as user_bp
        from app.admin import bp as admin_bp
        from app.password_recovery import bp as password_recovery_bp
        from app.error import bp as error_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(login_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(password_recovery_bp)
        app.register_blueprint(error_bp)

        login_bp.xcaptcha = xcaptcha

    return app
