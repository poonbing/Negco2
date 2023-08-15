# Python Modules
from flask import Flask
from flask_xcaptcha import XCaptcha
from flask_login import current_user
from .models import CartItem

import logging

# Local Modules
from config import Config
from .extensions import db, mail, login_manager, oauth, csrf, jwt, limiter
from .models import CartItem, Log
import secrets, stripe, os


def create_app(config_class=Config):
    app = Flask(__name__)
    # Whose is this??
    app.config.from_object(config_class)
    stripe_keys = {
        "secret_key": "sk_test_51NMQKILNkWku1TleBfxFFaU1PZExG7m5EWksDyd35bjyfoQlr71c0EBrNuD3bHFv37RL6Q0nvVuFbEZdRZ8MCruW00PyWCWL03",
        "publishable_key": "pk_test_51NMQKILNkWku1Tlem8G387xQhuNfG6cHSqzMhbIwLns7fBXX44qYnYyczyOfP7R3HbJE5sULy5kmtPb4PJpQyg0d00TvkHc0n1",
    }
    stripe.api_key = stripe_keys["secret_key"]

    @app.after_request
    def add_security_headers(response):
        response.headers[
            "Strict-Transport-Security"
        ] = "max-age=31536000; includeSubDomains; preload"
        response.headers[
            "Content-Security-Policy"
        ] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://d3js.org/d3.v7.min.js https://cdn.quilljs.com https://cdn.tailwindcss.com https://unpkg.com https://cdnjs.cloudflare.com/ajax/libs/flowbite/1.6.5/flowbite.min.js https://hcaptcha.com https://*.hcaptcha.com; style-src 'self' 'unsafe-inline' https://unpkg.com/ https://cdn.quilljs.com https://cdn.tailwindcss.com https://fonts.googleapis.com https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css https://cdnjs.cloudflare.com https://hcaptcha.com https://*.hcaptcha.com; font-src 'self' https://fonts.googleapis.com https://fonts.gstatic.com; connect-src 'self' https://unpkg.com https://assets.hcaptcha.com https://hcaptcha.com https://*.hcaptcha.com; frame-src 'self' https://assets.hcaptcha.com https://hcaptcha.com https://*.hcaptcha.com; img-src 'self' https://lh3.googleusercontent.com;"

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"

        return response

    @app.context_processor
    def cart_total_quantity():
        if current_user.is_authenticated:
            cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        else:
            cart_items = []
        total_quantity = sum(item.quantity for item in cart_items)
        return dict(cart_total_quantity=total_quantity)

    xcaptcha = XCaptcha(app=app)
    limiter.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    oauth.init_app(app)

    # with app.app_context():
    #     db.create_all()

    # Two Logging Mechanism
    class SQLAlchemyHandler(logging.Handler):
        def emit(self, record):
            try:
                extra_args = record.args
                log_text = record.msg.format(*extra_args)
                log_entry = Log(
                    source=record.__dict__.get("page", None),
                    logged_user=record.__dict__.get("user_id", None),
                    address=record.__dict__.get("address", None),
                    category=record.__dict__.get("category", None),
                    log_text=log_text,
                )
                print(log_entry.address, log_entry.logged_user)
                db.session.add(log_entry)
                db.session.commit()
            except Exception:
                self.handleError(record)

    handler = SQLAlchemyHandler()
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

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
    from app.report import bp as report_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(management_bp)
    app.register_blueprint(recovery_bp)
    app.register_blueprint(error_bp)
    app.register_blueprint(tracker_bp)
    app.register_blueprint(articles_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(forum_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    auth_bp.xcaptcha = xcaptcha

    # file_handler = logging.FileHandler(Config.LOG_FILE)
    # file_handler.setLevel(Config.LOG_LEVEL)
    # file_handler.setFormatter(Config.LOG_FORMAT)

    # app.logger.addHandler(file_handler)

    return app
