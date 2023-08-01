# Python Modules
from flask import render_template, request, url_for, session, redirect, flash, escape, Response, jsonify
from flask_login import current_user
from werkzeug.utils import secure_filename
from sqlalchemy import func, and_
from uuid import uuid4
import os
# checkout module
import datetime
import re
from decimal import Decimal
from decimal import getcontext



# Local Modules
from app.products import bp
from config import Config
from ..models import Products, CartItem, Checkout
from ..forms import createProduct, PaymentForm
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
    product_to_view = Products.query.get_or_404(id)
    if request.method == 'POST':
        rating = int(request.form['rating'])
        if not product_to_view.rating_score:
            product_to_view.rating_score = rating
            product_to_view.rating_count = 1
            db.session.commit()
            flash('Thank you for leaving a rating on the product!')
        else:
            product_to_view.rating_score += rating
            product_to_view.rating_count += 1
            db.session.commit()
            flash('Thank you for your rating on the product!')
    
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
    cart_item = CartItem.query.filter_by(product_id=product_id, user_id=current_user.id).first()

    if cart_item:
        cart_item.quantity += 1
        flash("Product quantity updated in cart!")
    else:
        if product.offered_price:
            cart_item = CartItem(
                id=str(uuid4())[:8], product_id=product_id, quantity=1, price=product.offered_price, user_id=current_user.id
            )
        else:
            cart_item = CartItem(
                id=str(uuid4())[:8], product_id=product_id, quantity=1, price=product.price, user_id=current_user.id
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


@bp.route("/update_quantity/<string:product_id>", methods=["GET", "POST"])
def update_quantity(product_id):
    csrf_token = request.form.get("csrf_token")
    quantity = int(request.form.get("quantity"))
    cart_item = CartItem.query.filter_by(product_id=product_id, user_id=current_user.id).first()


    if cart_item:
        cart_item.quantity = quantity
        db.session.commit()

    flash("Product quantity updated in cart!")
    return redirect(url_for("products.view_cart"))


@bp.route("/remove_from_cart/<string:product_id>")
def remove_from_cart(product_id):
    cart_item = CartItem.query.filter_by(product_id=product_id, user_id=current_user.id).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash("Product removed from cart successfully!")

    return redirect(url_for("products.view_cart"))



    
#payment Gateways
output = ""
def CheapPaymentGateway(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount):
    last4_cc = str(CreditCardNumber)[-4:]
    output = "\nProccessed Payment of ${:,.2f} for {} with CheapPaymentGateway, Card ending in {}\n".format(Amount, CardHolder, last4_cc)
    print(output)
    return (1, output)

def ExpensivePaymentGateway(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount):
    last4_cc = str(CreditCardNumber)[-4:]
    output = "\nProccessed Payment of ${:,.2f} for {} with ExpensivePaymentGateway, Card ending in {}\n".format(Amount, CardHolder, last4_cc)
    print(output)
    return (1, output)

def PremiumPaymentGateway(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount):
    last4_cc = str(CreditCardNumber)[-4:]
    output = "\nProccessed Payment of ${:,.2f} for {} with PremiumPaymentGateway, Card ending in {}\n".format(Amount, CardHolder, last4_cc)
    print(output)
    return (1, output)


#processPayment()
# - CreditCardNumber (mandatory, string, it should be a valid credit card number)
# - CardHolder: (mandatory, string)
# - ExpirationDate (mandatory, DateTime, it cannot be in the past)
# - SecurityCode (optional, string, 3 digits)
# - Amount (mandatory decimal, positive amount) - Capped to anything under a million

@bp.route("/paymentPage", methods=["GET", "POST"])
def processPayment():
    form = PaymentForm()
    total_price = 0
    user = current_user
    checkout_items = CartItem.query.filter_by(user_id=user.id).all()
    total_quantity = sum(item.quantity for item in checkout_items)
    total_price = sum(item.price * item.quantity for item in checkout_items)
    # for item in checkout_items:
    #     if item.offered_price:
    #         price = item.offered_price * item.quantity
    #         total_price += price
    #     else:
    #         price = item.price * item.quantity
    #         total_price += price

    if form.validate_on_submit():
        card_num = form.credit_card_number.data.strip().replace(" ","")
        card_holder = str(form.card_holder.data).strip().upper()
        expiry_date = form.expiration_date.data
        security_code = str(form.security_code.data)
        form.amount.data = total_price
        amount = form.amount.data

        card_num_len = len(card_num)

        try:
            #card number check
            #assumming that card number pass MOD 10 algorithm check for now
            if card_num_len in [13,15,16] and card_num.isdigit():
                #Visa Card
                if card_num_len == 16 and card_num.startswith('4'):
                    pass
                #MasterCard
                elif card_num_len == 16 and card_num.startswith('5'):
                    pass
                #AMEX
                elif card_num_len == 15 and (card_num.startswith('34') or card_num.startswith('37')):
                    pass
                #Discover
                elif card_num_len == 16 and card_num.startswith('6'):
                    pass
                else:
                    print("Invalid Card Number: {}\n".format(card_num))
                    return 'The request is invalid', 400
            
            card_num = int(card_num)
            print('Passed Card Num check')

            #CardHolder check
            # assumeing min/max 2-24 characters for first name and same for last name
            # min length 5: 2 characters for first name, 1 for space, 2 for last name

            if len(card_holder) > 4:
                verify_name2 = bool(re.match(r'^[A-Z]{2,24} [A-Z]{2,24}$', card_holder))
                print("Card Holder ({}) Verified: {}".format(card_holder,verify_name2))

                verify_name3 = bool(re.match(r'^[A-Z]{2,24} [A-Z]{2,24} [A-Z]{2,24}$', card_holder))
                print("Card Holder ({}) Verified: {}".format(card_holder,verify_name3))

                verify_name4 = bool(re.match(r'^[A-Z]{2,24} [A-Z]{2,24} [A-Z]{2,24} [A-Z]{2,24}$', card_holder))
                print("Card Holder ({}) Verified: {}".format(card_holder,verify_name4))

                if not verify_name2:
                    if not verify_name3:
                        if not verify_name4:
                            print("Card Holder Value Invalid!\n")
                            return 'The request is invalid', 400
                else:
                    print("Valid Card Holder")

            else:
                print("Card Holder Value Invalid!\n")
                return 'The request is invalid', 400
            

            #expiration check
            if type(expiry_date) is not datetime.date:
                print("Invalid Expiry Date: {}\n".format(expiry_date))
                #bad request
                return 'The request is invalid', 400
            

            # ====================
            # Amount Check
            # 1-2 decimal places should be present - invalid if more
            # Positive values only, example: 0.50, 1.51, 520.55
            # Max: 999999.99
            # ====================

            # Precision of digits which Decimal lib will use to return
            # any calculated number
            getcontext().prec = 8
            # Use regex to match what an amount would look like
            # Max amount is limited to 999999.99 (assumption)
            # 6 digits before & 2 after decimal
            if bool(re.match(r'^[0-9]{1,6}\.[0-9]{1,2}$', str(amount))):
                amount = Decimal(amount).quantize(Decimal('1.00'))
                print("Amount valid: {}".format(str(amount)))
            else:
                print("Amount Invalid: {}\n".format(str(amount)))
                #bad request
                return 'The request is invalid', 400
            

            #security code check
            if security_code:
                security_str = str(security_code).strip()

                if security_str.isdigit() and len(security_str) == 3:
                    print("Valid Security Code")
                    security_code = int(security_code)
                else:
                    print("Invalid Security Code: {}\n".format(str(security_code)))
                    return 'The request is invalid', 400
                
            #add to checkout database
            product_id = (item.product.id for item in checkout_items)
            product_price = (item.price for item in checkout_items)
            product_quantity = (item.quantity for item in checkout_items)
            
            
            checkout = Checkout(id=str(uuid4())[:8], user_id=user.id, product_list=str(list(product_id)), 
                                product_price=str(list(product_price)),
                                product_quantity=str(list(product_quantity)), 
                                total_cost=total_price)
            db.session.add(checkout)
            db.session.commit()
                
        except Exception as e:
            print("Exception Raised: {}\n".format(e))
            return 'Internal server error', 500
        
        retry = 0

        #Payment Proccessor
        #assuming payment processor has boolean return on successful payment

        if amount <= 20:
            ret, output = CheapPaymentGateway(card_num, card_holder, expiry_date, security_code, amount)
            if ret:
                #output = 'Payment is proccessed', 200
                return output, 200
            else:
                return 'Internal server error: PaymentProccessor Failed', 500

        elif 20 < amount < 501:
            while retry < 2:
                ret, output = ExpensivePaymentGateway(card_num, card_holder, expiry_date, security_code, amount)
                if ret:
                    #output = 'Payment is proccessed', 200
                    return output, 200
                else:
                    retry += 1
            
            print("Could not proccess payment with ExpensivePaymentGateway")
            return 'Internal server error: PaymentProcessor Failed', 500
        
        else:
            while retry < 3:
                ret, output = PremiumPaymentGateway(card_num, card_holder, expiry_date, security_code, amount)
                if ret:
                    #output = 'Payment is proccessed', 200
                    return output, 200
                else:
                    retry += 1
            print("Could not proccess payment with PremiumPaymentGateway")
            return 'Internal server error: PaymentProccessor Failed', 500

        
    
        
    return render_template('products/checkout.html', form=form, checkout_items=checkout_items,
        total_quantity=total_quantity,
        total_price=total_price)

        

