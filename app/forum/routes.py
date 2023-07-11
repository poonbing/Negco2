# Python Modules
from flask import render_template, redirect, url_for, request

# Local Modules
from app.forum import bp
from ..models import Comment, Post, Topic
from ..forms import Comment_Submission, Post_Submission
from ..extensions import db


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/forum")
def home():
    topics = Topic.query.all()
    return render_template("forum/Home.html", topic=topics)


@bp.route("/topics/<int:topic_id>/posts", methods=["GET", "POST"])
def topic_posts(topic_id):
    print("Topic ID:", topic_id)

    page = request.args.get("page", 1, type=int)
    post_list = Post.query.filter_by(topic_id=topic_id).paginate(per_page=4, page=page)
    topic = Topic.query.get(topic_id)
    print("Topic:", topic)

    form = Post_Submission()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data, content=form.content.data, topic_id=topic_id
        )
        db.session.add(new_post)
        try:
            db.session.commit()
        except Exception as e:
            print(f"An error occurred while committing the post: {e}")
        return redirect(url_for("topic_posts", topic_id=topic_id))

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
def post(id):
    db.session.rollback()
    comment_list = Comment.query.filter_by(post_id=id).all()
    print("testlist")
    form = Comment_Submission()
    if request.method == "POST":
        print(form.content.data)
        new_comment = Comment(post_id=id, content=form.content.data)
        print("Success")
        print(new_comment)
        db.session.add(new_comment)
        print(f"New comment added to the session: {new_comment}")
        try:
            db.session.commit()
            print("Comment committed successfully")
            return redirect(url_for("post", id=id))
        except Exception as e:
            print(f"An error occurred while committing the comment: {e}")

    post = Post.query.get(id)
    if post:
        return render_template(
            "forum/Comments.html", post=post, form=form, comment_list=comment_list
        )
    else:
        return render_template("error/404.html")
