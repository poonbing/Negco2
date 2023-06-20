from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer(), unique = True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(500))

    def __init__(self, title, description):
        self.title = title
        self.description = description

