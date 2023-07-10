from wtforms.validators import InputRequired, Email, Length, EqualTo
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    IntegerField,
    TextAreaField,
    FileField,
    SelectField,
    DecimalField,
    PasswordField,
)
from wtforms.validators import DataRequired


class SettingsForm(FlaskForm):
    profile_picture = FileField("Profile Picture")
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    phone = StringField("Phone Number", validators=[Length(min=8, max=16)])
    gender = StringField("Gender")
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password")
    confirm_password = PasswordField(
        "Confirm Password", validators=[EqualTo("password")]
    )


class createArticle(FlaskForm):
    title = StringField("Title of Article:", validators=[DataRequired()])
    description = TextAreaField(
        "Description:", validators=[DataRequired()], render_kw={"rows": 1}
    )
    writer = StringField("Writer:", validators=[DataRequired()])
    image = FileField("Image:", validators=[DataRequired()])
    paragraph = TextAreaField(
        "Paragraph:", validators=[DataRequired()], render_kw={"rows": 8}
    )
    submit = SubmitField("Submit")


class createProduct(FlaskForm):
    brand = StringField("Brand of Product:", validators=[DataRequired()])
    name = StringField("Name of Product:", validators=[DataRequired()])
    description = TextAreaField(
        "Description:", validators=[DataRequired()], render_kw={"rows": 4}
    )
    category = SelectField(
        "Category:", choices=[("On-the-go"), ("Kitchen"), ("Bathroom")]
    )
    price = DecimalField("Price of product($):", places=2, validators=[DataRequired()])
    offer = IntegerField("Offer(%)", validators=[DataRequired()])
    image = FileField("Image:", validators=[DataRequired()])
    submit = SubmitField("Submit")
