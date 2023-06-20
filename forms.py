from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, FileField, SelectField, DecimalField
from wtforms.validators import DataRequired


class createArticle(FlaskForm):

    title = StringField("Title of Article:", validators=[DataRequired()])
    description = TextAreaField("Description:", validators=[DataRequired()], render_kw={'rows':1})
    writer = StringField("Writer:", validators=[DataRequired()])
    image = FileField("Image:", validators=[DataRequired()])
    paragraph = TextAreaField("Paragraph:", validators=[DataRequired()], render_kw={'rows':8})
    submit = SubmitField("Submit")

class createProduct(FlaskForm):
    name = StringField("Name of Product:", validators=[DataRequired()])
    description = TextAreaField("Description:", validators=[DataRequired()], render_kw={'rows':4})
    category = SelectField("Category:", choices=[(1,'Hand & body'),(2,'Perfume & deodorant'),(3,'Accessories')])
    price = DecimalField("Price of product($):",places=2, validators=[DataRequired()])
    offer = IntegerField("Offer(%)", validators=[DataRequired()])
    image = FileField("Image:", validators=[DataRequired()])
    submit = SubmitField("Submit")