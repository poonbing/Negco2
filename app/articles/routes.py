# Python Modules
from flask import render_template, request, redirect, flash, url_for, current_app
from werkzeug.utils import secure_filename
from sqlalchemy import func
from uuid import uuid4
from config import Config
import os
from flask_login import login_required
# Local Modules
from app.articles import bp
from app.management.utils import role_required
from ..models import Articles
from ..forms import createArticle
from ..extensions import db
from app import limiter
import re
import bleach


def check_splcharacter(test): 
  
    # Make an RE character set and pass  
    # this as an argument in compile function
 
    string_check= re.compile('[@_!#$^&*<>?/\|}{~]') 
      
    # Pass the string in search function  
    # of RE object (string_check).
     
    if(string_check.search(test) == None): 
        print("String does not contain Special Characters.")
        return True
          
    else: 
        print("String contains Special Characters.") 
        return False

@bp.route("/allArticles")
@limiter.limit('5/second')
def allArticles():
    page = request.args.get("page", 1, type=int)
    articles = Articles.query.order_by(Articles.date_added.desc()).paginate(
        per_page=6, page=page
    )
    return render_template("articles/allArticles.html", articles=articles)


# retrieve individual article
@bp.route("/articlePage/<string:id>", methods=["GET", "POST"])
@limiter.limit('5/second')
def articlePage(id):
    article_to_view = Articles.query.get_or_404(id)
    more_article = Articles.query.order_by(func.random()).limit(3)
    return render_template(
        "articles/articlePage.html",
        article_to_view=article_to_view,
        more_article=more_article,
    )


# create article db
@bp.route("/publishArticle", methods=["POST", "GET"])
@login_required
@role_required("editor")
@limiter.limit('5/second')
def publishArticle():
    form = createArticle()
    if form.validate_on_submit():
        title = bleach.clean(form.title.data)
        description = bleach.clean(form.description.data)
        writer = bleach.clean(form.writer.data)
        paragraph = bleach.clean(form.paragraph.data)
        image = form.image.data
        image.save(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                Config.UPLOAD_FOLDER,
                secure_filename(image.filename),
            )
        )
        verify_characters = check_splcharacter(description)
        verify_characters2 = check_splcharacter(paragraph)
        if verify_characters:
            if verify_characters2:
                # grab image name
                image_name = secure_filename(image.filename)
                # add to db
                id=str(uuid4())[:8]
                article = Articles(
                    id=id,
                    title=title,
                    description=description,
                    writer=writer,
                    image=image_name,
                    paragraph=paragraph,
                )
                # current_app.logger.info(f'Article Published: {id}', extra={'user_id': 'editor', 'address': request.remote_addr, 'page': request.path, 'category':'Article'})
                db.session.add(article)
                db.session.commit()
                flash("Article added successfully!")
                return redirect(url_for("articles.viewArticle"))
        else:
            print("This data is suspicious.")

    return render_template("articles/publishArticle.html", form=form)


# retrieve article db
@bp.route("/viewArticle")
@limiter.limit('5/second')
@login_required
@role_required("editor")
def viewArticle():
    page = request.args.get("page", 1, type=int)
    articles = Articles.query.order_by(Articles.date_added.desc()).paginate(
        per_page=4, page=page
    )
    return render_template("articles/viewArticle.html", articles=articles)


@bp.route("/updateArticle/<string:id>", methods=["GET", "POST"])
@login_required
@role_required("editor")
@limiter.limit('5/second')
def updateArticle(id):
    form = createArticle()
    article_to_update = Articles.query.get_or_404(id)
    if request.method == "POST":
        # Update the article with the form data
        article_to_update.title = bleach.clean(form.title.data)
        article_to_update.description = bleach.clean(form.description.data)
        article_to_update.writer = bleach.clean(form.writer.data)
        article_to_update.paragraph = bleach.clean(form.paragraph.data)
        article_to_update.image = form.image.data
        verify_characters = check_splcharacter(article_to_update.description)
        verify_characters2 = check_splcharacter(article_to_update.paragraph)
        if verify_characters:
            if verify_characters2:
                # Save the updated article to the database
                try:
                    # current_app.logger.info(f'Article Updated: {id}', extra={'user_id': 'editor', 'address': request.remote_addr, 'page': request.path, 'category':'Article'})
                    db.session.commit()
                    flash("Article updated successfully!")
                    return redirect(url_for("articles.viewArticle"))

                except:
                    return "Oops! Looks like something went wrong."
        else:
            print("Data is suspicious")

    # Pre-fill the form fields with the article details
    form.title.data = article_to_update.title
    form.description.data = article_to_update.description
    form.writer.data = article_to_update.writer
    form.paragraph.data = article_to_update.paragraph
    form.image.data = article_to_update.image

    return render_template(
        "articles/updateArticle.html",
        form=form,
        article_to_update=article_to_update,
    )


# delete article db
@bp.route("/deleteArticle/<string:id>")
@login_required
@role_required("editor")
@limiter.limit('5/second')
def deleteArticle(id):
    article_to_delete = Articles.query.get_or_404(id)
    try:
        # current_app.logger.info(f'Article Deleted: {id}', extra={'user_id': 'editor', 'address': request.remote_addr, 'page': request.path, 'category':'Article'})
        db.session.delete(article_to_delete)
        db.session.commit()
        flash("Article deleted succesfully!")
        return redirect(url_for("articles.viewArticle"))
    except:
        return render_template(
            "articles/viewArticle.html", article_to_delete=article_to_delete
        )
