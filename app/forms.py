from flask_wtf import FlaskForm
import re
from wtforms.validators import (
    InputRequired,
    Email,
    Length,
    EqualTo,
    ValidationError,
    NumberRange,
    DataRequired,
)
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
    DateField,
)
import datetime
from wtforms_components import DateTimeField, DateRange
from flask_wtf.file import FileRequired, FileAllowed


def password_check(form, field):
    password = field.data

    length_error = len(password) < 8
    digit_error = not re.search(r"\d", password)
    uppercase_error = not re.search(r"[A-Z]", password)
    lowercase_error = not re.search(r"[a-z]", password)
    symbol_error = not re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password)

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
    title = StringField(
        "Title of Article:", validators=[InputRequired(), Length(min=3, max=100)]
    )
    description = TextAreaField(
        "Description:",
        validators=[InputRequired(), Length(min=3, max=300)],
        render_kw={"rows": 1},
    )
    writer = StringField("Writer:", validators=[InputRequired(), Length(min=3, max=50)])
    image = FileField(
        "Image:", validators=[FileRequired(), FileAllowed(["jpg", "jpeg", "png"])]
    )
    paragraph = TextAreaField(
        "Paragraph:",
        validators=[InputRequired(), Length(min=100, max=1000000)],
        render_kw={"rows": 30},
    )
    submit = SubmitField("Submit")


class createProduct(FlaskForm):
    brand = StringField(
        "Brand of Product:", validators=[InputRequired(), Length(min=2, max=50)]
    )
    name = StringField(
        "Name of Product:", validators=[InputRequired(), Length(min=3, max=50)]
    )
    description = TextAreaField(
        "Description:",
        validators=[InputRequired(), Length(min=10, max=1000)],
        render_kw={"rows": 8},
    )
    category = SelectField(
        "Category:", choices=[("On-the-go"), ("Kitchen"), ("Bathroom")]
    )
    price = DecimalField(
        "Price of product($):",
        places=2,
        validators=[InputRequired(), NumberRange(min=0, max=999)],
    )
    offer = IntegerField(
        "Offer(%)", validators=[InputRequired(), NumberRange(min=0, max=100)]
    )
    image = FileField(
        "Image:", validators=[FileRequired(), FileAllowed(["jpg", "jpeg", "png"])]
    )
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
    password = PasswordField("Password", validators=[InputRequired(), password_check])
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


class ForgotPasswordForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    submit = SubmitField("Submit")


class AccessCodeForm(FlaskForm):
    access_code = IntegerField(
        "Access Code", validators=[InputRequired(), NumberRange(min=100000, max=999999)]
    )
    submit = SubmitField("Submit")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired()])
    submit = SubmitField("Submit")


class ForgotPasswordForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    submit = SubmitField("Submit")


class AccessCodeForm(FlaskForm):
    access_code = IntegerField(
        "Access Code", validators=[InputRequired(), NumberRange(min=100000, max=999999)]
    )
    submit = SubmitField("Submit")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired()])
    submit = SubmitField("Submit")


class PaymentForm(FlaskForm):
    # Field types followed by label and data validators
    credit_card_number = StringField(
        "Card Details",
        [DataRequired(), Length(min=13, max=16, message="Invalid Credit Card Number")],
        render_kw={"placeholder": "xxxx-xxxx-xxxx-xxxx"},
    )
    card_holder = StringField(
        "Credit Card Holder",
        [DataRequired(), Length(min=5, max=49, message="Invalid Length")],
        render_kw={"placeholder": "Name on the Card"},
    )
    expiration_date = DateField(
        "Expiry Date (YYYY-MM-DD)",
        [
            DataRequired(),
            DateRange(
                min=datetime.datetime.today().date(), max=datetime.date(2030, 12, 31)
            ),
        ],
        format="%Y-%m-%d",
    )
    security_code = StringField(
        "CVC",
        [DataRequired(), Length(min=3, max=3, message="Length should be 3 digits")],
        render_kw={"placeholder": "CVC"},
    )
    amount = DecimalField("Subtotal")
    submit = SubmitField("Place Order")


class TrackerInteract(FlaskForm):
    name = StringField("Name: ", validators=[InputRequired()])
    item = StringField("Item: ", validators=[InputRequired()])
    rate = StringField("Rate: ", validators=[InputRequired(), Length(min=1, max=5)])
    action = StringField("action", validators=[InputRequired()])
    old_name = StringField("old name", validators=[InputRequired()])
    old_item = StringField("old item", validators=[InputRequired()])
