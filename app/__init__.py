# Python Modules
from flask import Flask
from flask_xcaptcha import XCaptcha


# Local Modules
from config import Config
from .extensions import db, mail, login_manager, oauth, csrf, jwt
from .models import CartItem
import logging


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    @app.after_request
    def add_security_headers(response):
        response.headers[
            "Strict-Transport-Security"
        ] = "max-age=31536000; includeSubDomains"
        # response.headers[
        #     "Content-Security-Policy"
        # ] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://unpkg.com https://cdnjs.cloudflare.com/ajax/libs/flowbite/1.6.5/flowbite.min.js https://hcaptcha.com https://assets.hcaptcha.com; style-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://fonts.googleapis.com https://cdn.quilljs.com https://unpkg.com https://cdnjs.cloudflare.com; font-src 'self' https://fonts.googleapis.com https://fonts.gstatic.com; connect-src https://assets.hcaptcha.com; frame-src https://assets.hcaptcha.com; script-src https://hcaptcha.com https://assets.hcaptcha.com;"

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"

        return response

    @app.context_processor
    def cart_total_quantity():
        cart_items = CartItem.query.all()
        total_quantity = sum(item.quantity for item in cart_items)
        return dict(cart_total_quantity=total_quantity)

    xcaptcha = XCaptcha(app=app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    oauth.init_app(app)

    oauth.register(
        name="google",
        client_id=Config.GOOGLE_CLIENT_ID,
        client_secret=Config.GOOGLE_CLIENT_SECRET,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    oauth.register(
        name="azure",
        client_id=Config.AZURE_CLIENT_ID,
        client_secret=Config.AZURE_CLIENT_SECRET,
        api_base_url="https://graph.microsoft.com/",
        server_metadata_url="https://login.microsoftonline.com/f8cdef31-a31e-4b4a-93e4-5f571e91255a/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    from app.main import bp as main_bp
    from app.auth import bp as auth_bp

    from app.management import bp as management_bp
    from app.recovery import bp as recovery_bp
    from app.error import bp as error_bp
    from app.api import bp as api_bp
    from app.tracker import bp as tracker_bp
    from app.articles import bp as articles_bp
    from app.products import bp as products_bp
    from app.forum import bp as forum_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(management_bp)
    app.register_blueprint(recovery_bp)
    app.register_blueprint(error_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(tracker_bp)
    app.register_blueprint(articles_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(forum_bp)

    auth_bp.xcaptcha = xcaptcha

    file_handler = logging.FileHandler(Config.LOG_FILE)
    file_handler.setLevel(Config.LOG_LEVEL)
    file_handler.setFormatter(Config.LOG_FORMAT)

    app.logger.addHandler(file_handler)

    return app
