import re
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
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


def password_check(form, field):
    password = field.data

    length_error = len(password) < 8
    digit_error = re.search(r"\d", password is None)
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None

    if (
        length_error
        or digit_error
        or uppercase_error
        or lowercase_error
        or symbol_error
    ):
        raise ValidationError(
            "Password must be at least 8 characters long and contain at least one digit, one uppercase letter, one lowercase letter, and one symbol."
        )


class SettingsForm(FlaskForm):
    profile_picture = FileField("Profile Picture")
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    phone = StringField("Phone Number", validators=[Length(min=8, max=16)])
    gender = SelectField(
        "Gender", choices=[("male", "Male"), ("female", "Female"), ("other", "Other")]
    )
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
