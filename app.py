
from flask import Flask, render_template, request, url_for, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, func, ForeignKey
from datetime import datetime
from forms import createArticle, createProduct
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
#configure db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///article.db'
app.config['SQLALCHEMY_BINDS'] = {'two': 'sqlite:///product.db'}
				  				
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "app security project"
app.config['UPLOAD_FOLDER'] = 'static/images'
#initialize the database
db = SQLAlchemy(app)

#create Model
class Articles(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(50), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.today)
    writer = db.Column(db.String(20), nullable=False) 
    image = db.Column(db.String(), unique=True, nullable=False)
    paragraph = db.Column(db.String(500), nullable=False)

    #create a string
    def __repr__(self):
        return '<Title %r>' % self.title



class Products(db.Model):
	__tablename__ = 'products'
	__bind_key__ = 'two'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False, unique=True)
	description = db.Column(db.String(200), nullable=False)
	category = db.Column(db.String(20), nullable=False)
	price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
	offer = db.Column(db.Integer)
	image = db.Column(db.String(), unique=True, nullable=False) 
	date_added = db.Column(db.DateTime, default=datetime.today)

	

#homepage
@app.route("/")
def index():
	articles = Articles.query.order_by(desc(Articles.date_added)).limit(4)
	products = Products.query.order_by(desc(Products.date_added)).limit(6)
	total_quantity = get_total_quantity()
	return render_template("index.html", articles=articles, products=products, total_quantity=total_quantity)



@app.route("/allArticles")
def allArticles():
	articles = Articles.query.order_by(desc(Articles.date_added))	 
	return render_template("allArticles.html", articles=articles)


#retrieve individual article
@app.route("/articlePage/<int:id>",  methods = ['GET', 'POST'])
def articlePage(id):
	article_to_view = Articles.query.get_or_404(id)
	more_article = Articles.query.order_by(func.random()).limit(2)
	return render_template('articlePage.html', article_to_view=article_to_view, more_article=more_article)



#create article db
@app.route('/publishArticle', methods = ['POST', 'GET'])
def publishArticle():
	form = createArticle()
	if request.method == 'POST':
		title = form.title.data
		description = form.description.data
		writer = form.writer.data
		paragraph = form.paragraph.data
		image = form.image.data
		image.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
		#grab image name
		image_name = secure_filename(image.filename)
		#add to db
		article = Articles(title=title, description=description, writer=writer, image=image_name, paragraph=paragraph)
		db.session.add(article)
		db.session.commit()
		flash('Article added successfully!')
		return redirect('/viewArticle')
	return render_template('publishArticle.html', form = form)

#retrieve article db
@app.route('/viewArticle')
def viewArticle():
	articles = Articles.query.all()
	return render_template('viewArticle.html', articles = articles)


#update article db
@app.route('/updateArticle/<int:id>', methods = ['GET', 'POST'])
def updateArticle(id):
	form = createArticle()
	article_to_update = Articles.query.get_or_404(id)
	if request.method == 'POST':
		article_to_update.title = form.title.data
		article_to_update.description = form.description.data
		article_to_update.writer = form.writer.data
		article_to_update.image = form.image.data
		article_to_update.paragraph = form.paragraph.data
		try:
			db.session.commit()
			flash('Article updated successfully!')
			return redirect('/viewArticle')
		except:
			return "Opps! Looks like something went wrong."
	else:
		return render_template('updateArticle.html', form=form, article_to_update=article_to_update)

#delete article db
@app.route('/deleteArticle/<int:id>')
def deleteArticle(id):
	article_to_delete = Articles.query.get_or_404(id)
	try:
		db.session.delete(article_to_delete)
		db.session.commit()
		flash('Article deleted succesfully!')
		return redirect('/viewArticle')
	except:
		return render_template('viewArticle.html', article_to_delete=article_to_delete)


@app.route('/createProduct', methods = ['POST', 'GET'])
def publishProduct():
	form = createProduct()
	if request.method == 'POST':
		name = form.name.data
		description = form.description.data
		category = form.category.data
		price = form.price.data
		offer = form.offer.data
		image = form.image.data
		image.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
		#grab image name
		image_name = secure_filename(image.filename)
		#add to db
		product = Products(name=name, description=description, category=category, price=price, offer=offer, image=image_name)
		db.session.add(product)
		db.session.commit()
		flash('Product added successfully!')
		return redirect('/viewProduct')
	return render_template('createProduct.html', form = form)


@app.route('/viewProduct')
def viewProduct():
	products = Products.query.all()
	return render_template('viewProduct.html', products=products)


@app.route('/updateProduct/<int:id>', methods = ['GET', 'POST'])
def updateProduct(id):
	form = createProduct()
	product_to_update = Products.query.get_or_404(id)
	if request.method == 'POST':
		product_to_update.name = form.name.data
		product_to_update.description = form.description.data
		product_to_update.price = form.price.data
		product_to_update.image = form.image.data
		product_to_update.offer = form.offer.data
		product_to_update.category = form.category.data
		try:
			db.session.commit()
			flash('Product updated successfully!')
			return redirect('/viewProduct')
		except:
			return "Opps! Looks like something went wrong."
	else:
		return render_template('updateProduct.html', form=form, product_to_update=product_to_update)



@app.route('/deleteProduct/<int:id>')
def deleteProduct(id):
	product_to_delete = Products.query.get_or_404(id)
	try:
		db.session.delete(product_to_delete)
		db.session.commit()
		flash('Product deleted succesfully!')
		return redirect('/viewProduct')
	except:
		return render_template('viewProduct.html', product_to_delete=product_to_delete)


@app.route("/productPage/<int:id>",  methods = ['GET', 'POST'])
def productPage(id):
	product_to_view = Products.query.get_or_404(id)
	more_product = Products.query.order_by(func.random()).limit(3)

	return render_template('productPage.html', product_to_view=product_to_view, more_product=more_product)


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []

    # Check if the product already exists in the cart
    for item in session['cart']:
        if item['product_id'] == product_id:
            item['quantity'] += 1
            flash('Product quantity updated in cart!')
            return redirect(request.referrer)

    # If the product doesn't exist in the cart, add it with a quantity of 1
    product = {'product_id': product_id, 'quantity': 1}
    session['cart'].append(product)
    flash('Product added to cart successfully!')
    return redirect(request.referrer)


# ...

@app.route('/view_cart')
def view_cart():
    if 'cart' not in session:
        session['cart'] = []
    
    cart_items = []
    total_quantity = 0
    total_price = 0

    for item in session['cart']:
        product_id = item['product_id']
        quantity = item['quantity']
        
        product = Products.query.get(product_id)
        subtotal = quantity * product.price

        cart_item = {
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        }

        cart_items.append(cart_item)
        total_quantity += quantity
        total_price += subtotal

    return render_template('viewCart.html', cart_items=cart_items, total_quantity=total_quantity, total_price=total_price)

# ...

@app.route('/update_quantity/<int:product_id>', methods=['POST'])
def update_quantity(product_id):
    quantity = int(request.form.get('quantity'))

    # Find the product in the cart and update its quantity
    for item in session['cart']:
        if item['product_id'] == product_id:
            item['quantity'] = quantity
            flash('Product quantity updated in cart!')
            break

    return redirect(url_for('view_cart'))



@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []

    # Find the product in the cart and remove it
    session['cart'] = [item for item in session['cart'] if item['product_id'] != product_id]

    flash('Product removed from cart successfully!')
    return redirect(url_for('view_cart'))



def get_total_quantity():
    if 'cart' not in session:
        session['cart'] = []

    total_quantity = 0
    cart_items = session['cart']
    for item in cart_items:
        total_quantity += item['quantity']

    return total_quantity

@app.route('/allProducts', methods=['GET', 'POST'])
def allProducts():
	products = Products.query.all()
	return render_template('allProducts.html', products=products)	
 
@app.route('/filterProducts/<string:category>', methods=['GET', 'POST'])
def filterProducts(category):
    products = Products.query.filter_by(category=category).all()
    return render_template('filteredProducts.html', products=products)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
	app.run(debug=True)