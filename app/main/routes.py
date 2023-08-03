# Python Modules
from flask import render_template
from sqlalchemy import desc, not_
from flask_login import current_user

# Local Modules
from app.main import bp
from ..models import Products, Articles, Post


@bp.route("/")
def index():
    articles = Articles.query.order_by(desc(Articles.date_added)).limit(3)
    products = Products.query.order_by(desc(Products.date_added)).limit(4)
    return render_template("main/index.html", articles=articles, products=products)
