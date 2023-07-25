# Python Modules
from flask import Flask, session
from flask_xcaptcha import XCaptcha
from flask_login import current_user
from .models import CartItem
# Local Modules
from config import Config
from .extensions import db, mail, login_manager, oauth, talisman
from .models import CartItem


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # talisman.init_app(app)
    xcaptcha = XCaptcha(app=app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
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
        if current_user.is_authenticated:
            cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        else:
            cart_items = []
        total_quantity = sum(item.quantity for item in cart_items)
        return dict(cart_total_quantity=total_quantity)

    from app.main import bp as main_bp
    from app.auth import bp as auth_bp
    from app.auth import google_blueprint
    from app.auth import github_blueprint
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
    app.register_blueprint(google_blueprint, url_prefix="/login")
    app.register_blueprint(github_blueprint, url_prefix="/login")

    auth_bp.xcaptcha = xcaptcha

    return app
