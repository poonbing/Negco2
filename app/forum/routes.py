# Python Modules
from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_required

# Local Modules
from app import limiter
from app.forum import bp
from .utils import remove_html_tags
from ..models import Comment, Post, Topic
from ..forms import Comment_Submission, Post_Submission
from ..extensions import db


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/forum")
@limiter.limit('4/second')
def home():
    topics = Topic.query.all()
    return render_template("forum/Home.html", topic=topics)


@bp.route("/topics/<int:topic_id>/posts", methods=["GET", "POST"])
@login_required
@limiter.limit('4/second')
def topic_posts(topic_id):
    print("Topic ID:", topic_id)

    page = request.args.get("page", 1, type=int)
    post_list = Post.query.filter_by(topic_id=topic_id).paginate(per_page=4, page=page)
    topic = Topic.query.get(topic_id)
    print("Topic:", topic)

    form = Post_Submission()
    if form.validate_on_submit():
        user = current_user
        new_post = Post(
            poster=user.id,
            title=form.title.data,
            content=remove_html_tags(form.content.data),
            topic_id=topic_id,
        )
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
        )
    else:
        return render_template("error/404.html")


@bp.route("/post/<int:id>/", methods=["GET", "POST"])
@login_required
@limiter.limit('4/second')
def post(id):
    db.session.rollback()
    comment_list = Comment.query.filter_by(post_id=id).all()
    print("testlist")
    form = Comment_Submission()
    if form.validate_on_submit():
        user = current_user
        new_comment = Comment(
            commenter=user.id, post_id=id, content=remove_html_tags(form.content.data)
        )
        print("Success")
        print(new_comment)
        db.session.add(new_comment)
        print(f"New comment added to the session: {new_comment}")
        try:
            db.session.commit()
            print("Comment committed successfully")
            return redirect(url_for("forum.post", id=id))
        except Exception as e:
            print(f"An error occurred while committing the comment: {e}")

    post = Post.query.get(id)
    if post:
        return render_template(
            "forum/Comments.html", post=post, form=form, comment_list=comment_list
        )
    else:
        return render_template("error/404.html")
