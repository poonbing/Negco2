# Python Modules
from flask import Flask
from flask_xcaptcha import XCaptcha
from flask_login import current_user
from .models import CartItemfrom 
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
# Local Modules
from config import Config
from .extensions import db, mail, login_manager, oauth, csrf, jwt
from .models import CartItem, Log
from flask_wtf.csrf import CSRFProtect
import secrets

                  #storage_uri="mysql+mysqlconnector://Negco_Admin:Forehead_Gang@it2555.mysql.database.azure.com/neggo2")
limiter = Limiter(key_func=get_remote_address)

def create_app(config_class=Config):
    app = Flask(__name__)
    key = secrets.token_urlsafe(16)
    csrf = CSRFProtect()
    app.config['SECRET_KEY'] = key
    app.config.from_object(config_class)
    limiter.init_app(app)
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
        if current_user.is_authenticated:
            cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        else:
            cart_items = []
        total_quantity = sum(item.quantity for item in cart_items)
        return dict(cart_total_quantity=total_quantity)

    xcaptcha = XCaptcha(app=app)
    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    oauth.init_app(app)

    with app.app_context():
        db.create_all()

        # def get_total_quantity():
    #     if "cart" not in session:
    #         return 0

    #     total_quantity = 0
    #     cart_items = session["cart"]
    #     for item in cart_items:
    #         total_quantity += item["quantity"]

    #     return total_quantity

    # @app.context_processor
    # def inject_total_quantity():
    #     total_quantity = get_total_quantity()
    #     return dict(total_quantity=total_quantity)
    @app.context_processor
    def cart_total_quantity():
        cart_items = CartItem.query.all()
        total_quantity = sum(item.quantity for item in cart_items)
        return dict(cart_total_quantity=total_quantity)

    class SQLAlchemyHandler(logging.Handler):
        def emit(self, record):
            log_entry = Log(log_text=self.format(record))
            db.session.add(log_entry)
            db.session.commit()

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

    file_handler = logging.FileHandler(Config.LOG_FILE)
    file_handler.setLevel(Config.LOG_LEVEL)
    file_handler.setFormatter(Config.LOG_FORMAT)

    app.logger.addHandler(file_handler)

    return app
