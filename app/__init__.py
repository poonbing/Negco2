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
    from app.auth import bp as auth_bp
    from app.management import bp as management_bp
    from app.recovery import bp as recovery_bp
    from app.error import bp as error_bp
    from app.api import bp as api_bp

    # from app.tracker import bp as tracker_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(management_bp)
    app.register_blueprint(recovery_bp)
    app.register_blueprint(error_bp)
    app.register_blueprint(api_bp)
    # app.register_blueprint(tracker_bp)

    auth_bp.xcaptcha = xcaptcha

    return app
