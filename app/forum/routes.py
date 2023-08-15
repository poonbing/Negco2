# Python Modules
from flask import render_template, redirect, url_for, request, current_app
from flask_login import current_user, login_required
import os
# Local Modules
from app import limiter
from app.forum import bp
from .utils import remove_html_tags
from ..models import Comment, Post, Topic
from ..forms import Comment_Submission, Post_Submission
from ..extensions import db
from werkzeug.utils import secure_filename
from config import Config



def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/test")
def test():
    return render_template("forum/test.html")


@bp.route("/test1")
def test2():
    return render_template("forum/test1.html")


@bp.route("/forum")
@limiter.limit("4/second")
def home():
    topics = Topic.query.all()
    return render_template("forum/Home.html", topic=topics)


@bp.route("/topics/<int:topic_id>/posts", methods=["GET", "POST"])
@login_required
@limiter.limit("4/second")
def topic_posts(topic_id):
    print("Topic ID:", topic_id)

    page = request.args.get("page", 1, type=int)
    post_list = Post.query.filter_by(topic_id=topic_id).paginate(per_page=1, page=page)
    topic = Topic.query.get(topic_id)
    topic_title = topic.name
    print("Topic:", topic)

    form = Post_Submission()
    if form.validate_on_submit():
        user = current_user
        new_post = Post(
            poster=user.id,
            poster_username=user.username,
            title=form.title.data,
            content=remove_html_tags(form.content.data),
            topic_id=topic_id
        )
        if form.image.data:
            # Save the image as a file on the server
            file = form.image.data
            filename = secure_filename(file.filename)
            print(filename)
            image = form.image.data
            image.save(os.path.join(Config.UPLOAD_FOLDER,secure_filename(image.filename)))
            print(current_app)
            print(image)
            new_post.image = filename
        db.session.add(new_post)
        try:
            db.session.commit()
        except Exception as e:
            print(f"An error occurred while committing the post: {e}")
        return redirect(url_for("forum.topic_posts", topic_id=topic_id))

    if topic:
        return render_template(
            "forum/Posts.html",
            topic=topic,
            post_list=post_list,
            form=form,
            topic_id=topic_id,
            topic_title=topic_title
        )
    else:
        return render_template("error/404.html")


@bp.route("/post/<int:id>/", methods=["GET", "POST"])
@login_required
def post(id):
    db.session.rollback()
    comment_list = Comment.query.filter_by(post_id=id).all()
    post = Post.query.filter_by(id=id).first()
    print("testlist")
    form = Comment_Submission()
    print("test2")

    if form.validate_on_submit():
        print("Form image data:", form.image.data)
        print("test3")
        user = current_user

        print(type(current_user))
        print("test4")
        new_comment = Comment(commenter=user.id, commenter_username=user.username, post_id=id, content=remove_html_tags(form.content.data))
        if form.image.data:
            print("Image data:", form.image.data.filename)
            # Save the image as a file on the server
            filename = secure_filename(form.image.data.filename)
            print(filename)
            image = form.image.data
            image.save(os.path.join(Config.UPLOAD_FOLDER,secure_filename(image.filename)))
            print(current_app)
            print(image)
            new_comment.image = filename
        print("Success")
        print(new_comment)
        if post.no_of_comments == None:
            post.no_of_comments = 1
        else:
            post.no_of_comments += 1

        db.session.add(new_comment)
        print(f"New comment added to the session: {new_comment}")
        try:
            db.session.commit()
            print("Comment committed successfully")
            return redirect(url_for("forum.post", id=id))
        except Exception as e:
            print(f"An error occurred while committing the comment: {e}")
    db.session.rollback()
    post = Post.query.get(id)
    if post:
        return render_template(
            "forum/Comments.html", post=post, form=form, comment_list=comment_list, current_user = current_user
        )
    else:
        return render_template("error/404.html")
