from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Length, EqualTo
from wtforms import (
    StringField,
    SubmitField,
    IntegerField,
    TextAreaField,
    FileField,
    SelectField,
    DecimalField,
    PasswordField,
    BooleanField,
)


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
    title = StringField("Title of Article:", validators=[InputRequired()])
    description = TextAreaField(
        "Description:", validators=[InputRequired()], render_kw={"rows": 1}
    )
    writer = StringField("Writer:", validators=[InputRequired()])
    image = FileField("Image:", validators=[InputRequired()])
    paragraph = TextAreaField(
        "Paragraph:", validators=[InputRequired()], render_kw={"rows": 8}
    )
    submit = SubmitField("Submit")


class createProduct(FlaskForm):
    brand = StringField("Brand of Product:", validators=[InputRequired()])
    name = StringField("Name of Product:", validators=[InputRequired()])
    description = TextAreaField(
        "Description:", validators=[InputRequired()], render_kw={"rows": 4}
    )
    category = SelectField(
        "Category:", choices=[("On-the-go"), ("Kitchen"), ("Bathroom")]
    )
    price = DecimalField("Price of product($):", places=2, validators=[InputRequired()])
    offer = IntegerField("Offer(%)", validators=[InputRequired()])
    image = FileField("Image:", validators=[InputRequired()])
    submit = SubmitField("Submit")


class Comment_Submission(FlaskForm):
    content = TextAreaField("Content", validators=[InputRequired()])
    submit = SubmitField("Create Post")


class Post_Submission(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content", validators=[InputRequired()])
    submit = SubmitField("Create Post")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    remember = BooleanField("Remember me")


class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    gender = SelectField(
        "Gender",
        choices=[("Male"), ("Female")],
        validators=[InputRequired()],
    )
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    age = IntegerField("Age", validators=[InputRequired()])
    phone = StringField("Phone", validators=[InputRequired()])

class TrackerInteract(FlaskForm):
    name = StringField("Name: ", validators=[InputRequired()])
    item = StringField("Item: ", validators=[InputRequired()])
    rate = StringField("Rate: ", validators=[InputRequired(), Length(min=1, max=5)])
    action = StringField("action", validators=[InputRequired()])
    old_name = StringField("old name", validators=[InputRequired()])
    old_item = StringField("old item", validators=[InputRequired()])