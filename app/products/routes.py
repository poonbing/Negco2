# Python Modules
from flask import render_template, request, url_for, session, redirect, flash
from flask_login import current_user
from werkzeug.utils import secure_filename
from sqlalchemy import func
from uuid import uuid4
import os

# Local Modules
from app.products import bp
from config import Config
from ..models import Products, CartItem
from ..forms import createProduct
from ..extensions import db


@bp.route("/createProduct", methods=["POST", "GET"])
def publishProduct():
    form = createProduct()
    if request.method == "POST":
        brand = form.brand.data
        name = form.name.data
        description = form.description.data
        category = form.category.data
        price = form.price.data
        offer = form.offer.data
        image = form.image.data
        image.save(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                Config.UPLOAD_FOLDER,
                secure_filename(image.filename),
            )
        )
        # grab image name
        image_name = secure_filename(image.filename)
        if offer > 0:
            offered_price = price - (price * offer / 100)
            # add to db
            product = Products(
                id=str(uuid4())[:8],
                brand=brand,
                name=name,
                description=description,
                category=category,
                price=price,
                offer=offer,
                image=image_name,
                offered_price=round(offered_price, 2),
            )
            db.session.add(product)
            db.session.commit()
            flash("Product added successfully!")
            return redirect(url_for("products.viewProduct"))

        else:
            # add to db
            product = Products(
                id=str(uuid4())[:8],
                brand=brand,
                name=name,
                description=description,
                category=category,
                price=price,
                offer=offer,
                image=image_name,
                offered_price=None,
            )
            db.session.add(product)
            db.session.commit()
            flash("Product added successfully!")
            return redirect(url_for("products.viewProduct"))

    return render_template("products/createProduct.html", form=form)


@bp.route("/viewProduct")
def viewProduct():
    page = request.args.get("page", 1, type=int)
    products = Products.query.order_by(Products.date_added.desc()).paginate(
        per_page=4, page=page
    )
    return render_template("products/viewProduct.html", products=products)


@bp.route("/updateProduct/<string:id>", methods=["GET", "POST"])
def updateProduct(id):
    form = createProduct()
    product_to_update = Products.query.get_or_404(id)
    if request.method == "POST":
        product_to_update.name = form.name.data
        product_to_update.description = form.description.data
        product_to_update.price = form.price.data
        product_to_update.image = form.image.data
        product_to_update.offer = form.offer.data
        product_to_update.category = form.category.data

        if product_to_update.offer > 0:
            product_to_update.offered_price = round(
                product_to_update.price
                - (product_to_update.price * product_to_update.offer / 100),
                2,
            )
        else:
            product_to_update.offered_price = None
        try:
            db.session.commit()
            flash("Product updated successfully!")
            return redirect(url_for("products.viewProduct"))

        except:
            return "Opps! Looks like something went wrong."
    else:
        form.name.data = product_to_update.name
        form.description.data = product_to_update.description
        form.price.data = product_to_update.price
        form.image.data = product_to_update.image
        form.offer.data = product_to_update.offer
        form.category.data = product_to_update.category
    return render_template(
        "products/updateProduct.html", form=form, product_to_update=product_to_update
    )


@bp.route("/deleteProduct/<string:id>")
def deleteProduct(id):
    product_to_delete = Products.query.get_or_404(id)
    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        flash("Product deleted succesfully!")
        return redirect(url_for("products.viewProduct"))

    except:
        return render_template(
            "products/viewProduct.html", product_to_delete=product_to_delete
        )


@bp.route("/productPage/<string:id>", methods=["GET", "POST"])
def productPage(id):
    # cart_items = []
    # if 'add_to_cart' in request.form:
    #     if "cart" not in session:
    #         session["cart"] = []
    #         # Check if the product already exists in the cart
    #     for item in session["cart"]:
    #         product_id = item["product_id"]
    #         quantity = item["quantity"]
    #         if item["product_id"] == id:
    #             item["quantity"] += 1
    #             flash("Product quantity updated in cart!")
    #             return redirect(request.referrer)

    #         product = Products.query.get(product_id)
    #         cart_item = CartItem(
    #         product_id=product.id, quantity=quantity, price=product.price
    #         )
    #         db.session.add(cart_item)
    #         db.session.commit()

    #         cart_items.append(cart_item)

    #     # If the product doesn't exist in the cart, add it with a quantity of 1
    #     product = {"product_id": id, "quantity": 1}
    #     session["cart"].append(product)

    #     flash("Product added to cart successfully!")

    product_to_view = Products.query.get_or_404(id)
    more_product = Products.query.order_by(func.random()).limit(4)

    return render_template(
        "products/productPage.html",
        product_to_view=product_to_view,
        more_product=more_product,
    )


@bp.route("/allProducts", methods=["GET", "POST"])
def allProducts():
    page = request.args.get("page", 1, type=int)
    products = Products.query.paginate(per_page=4, page=page)
    return render_template("products/allProducts.html", products=products)


@bp.route("/filterProducts/<string:category>", methods=["GET", "POST"])
def filterProducts(category):
    page = request.args.get("page", 1, type=int)
    products = Products.query.filter_by(category=category).paginate(
        per_page=4, page=page
    )
    return render_template(
        "products/filteredProducts.html", products=products, category=category
    )


@bp.route("/add_to_cart/<string:product_id>")
def add_to_cart(product_id):
    product = Products.query.get_or_404(product_id)
    cart_item = CartItem.query.filter_by(product_id=product_id).first()

    if cart_item:
        cart_item.quantity += 1
        flash("Product quantity updated in cart!")
    else:
        cart_item = CartItem(
            id=str(uuid4())[:8],
            product_id=product_id,
            quantity=1,
            price=product.price,
            user_id=current_user.id,
        )
        db.session.add(cart_item)
        flash("Product added to cart successfully!")

    db.session.commit()
    return redirect(request.referrer)


@bp.route("/view_cart")
def view_cart():
    user = current_user
    cart_items = CartItem.query.filter_by(user_id=user.id).all()

    total_quantity = sum(item.quantity for item in cart_items)
    total_price = sum(item.price * item.quantity for item in cart_items)

    return render_template(
        "products/viewCart.html",
        cart_items=cart_items,
        total_quantity=total_quantity,
        total_price=total_price,
    )


@bp.route("/update_quantity/<string:product_id>", methods=["POST"])
def update_quantity(product_id):
    quantity = int(request.form.get("quantity"))
    cart_item = CartItem.query.filter_by(product_id=product_id).first()

    if cart_item:
        cart_item.quantity = quantity
        db.session.commit()

    flash("Product quantity updated in cart!")
    return redirect(url_for("products.view_cart"))


@bp.route("/remove_from_cart/<string:product_id>")
def remove_from_cart(product_id):
    cart_item = CartItem.query.filter_by(product_id=product_id).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash("Product removed from cart successfully!")

    return redirect(url_for("products.view_cart"))


@bp.route("/checkoutPage", methods=["GET", "POST"])
def checkout():
    return render_template("products/checkout.html")
