from flask_wtf import FlaskForm
from wtforms.validators import (
    InputRequired,
    Email,
    Length,
    EqualTo,
    ValidationError,
    NumberRange,
    DataRequired,
    Regexp,
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
    RadioField,
    FloatField,
)
import datetime
from wtforms_components import DateRange
from flask_wtf.file import FileRequired, FileAllowed
import re
from .validators import *


# def validate_image(_, field):
#      mime = magic.Magic()
#      mime_type = mime.from_buffer(field.data.read(1024))

#      if not mime_type.startswith("image/jpeg") and not mime_type.startswith("image/png"):
#          raise ValidationError("File is not an allowed image type")

def no_special_characters(form, field):
    if re.search(r"[~\!@#$%^&*()_+{}\":;'\[\]]", field.data):
        raise ValidationError("Special characters are not allowed.")

def validate_password(_, field):
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


class UnlockAccountForm(FlaskForm):
    unlock_account = BooleanField("Unlock Account")
    submit = SubmitField("Unlock Selected Accounts")


class SettingsForm(FlaskForm):
    profile_picture = FileField(
        "Profile Picture",
        validators=[
            FileAllowed(["jpg", "png"], "Only JPG and PNG images allowed."),
            validate_image,
        ],
    )
    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(min=1, max=100), validate_name],
    )
    last_name = StringField(
        "Last Name", validators=[InputRequired(), Length(min=1, max=100), validate_name]
    )
    phone = StringField("Phone Number", validators=[Length(min=8, max=16)])
    gender = SelectField(
        "Gender", choices=[("male", "Male"), ("female", "Female"), ("other", "Other")]
    )
    email = StringField("Email", validators=[Length(min=2, max=250), Email()])
    password = PasswordField("Password", validators=[])
    confirm_password = PasswordField(
        "Confirm Password", validators=[EqualTo("password")]
    )
    submit = SubmitField("Submit")


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
        "Brand of Product:", validators=[InputRequired(), Length(min=2, max=50), no_special_characters]
    )
    name = StringField(
        "Name of Product:", validators=[InputRequired(), Length(min=3, max=50), no_special_characters]
    )
    description = TextAreaField(
        "Description:",
        validators=[InputRequired(), Length(min=10, max=2000)],
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
    image = FileField("Image", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    submit = SubmitField("Create Post")


class Post_Submission(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content", validators=[InputRequired()])
    image = FileField("Image", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    submit = SubmitField("Create Post")


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=100)],
    )
    password = PasswordField("Password", validators=[InputRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class SignUpForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), validate_username],
    )
    password = PasswordField(
        "Password", validators=[InputRequired(), validate_password]
    )

    confirm_password = PasswordField(
        "Confirm Password", validators=[EqualTo("password")]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    gender = SelectField(
        "Gender",
        choices=[("Male"), ("Female")],
        validators=[InputRequired()],
    )
    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(min=1, max=100), validate_name],
    )
    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(min=1, max=100), validate_name],
    )
    age = IntegerField(
        "Age",
        validators=[
            InputRequired(),
            NumberRange(min=0, max=200, message="Age must be between 0 and 200."),
        ],
    )
    phone = StringField("Phone", validators=[InputRequired(), validate_phone])
    submit = SubmitField("Sign Up")


class ForgotPasswordForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    submit = SubmitField("Submit")


class AccessCodeForm(FlaskForm):
    access_code = IntegerField(
        "Access Code", validators=[InputRequired(), NumberRange(min=100000, max=999999)]
    )
    submit = SubmitField("Submit")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password", validators=[InputRequired(), validate_password]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
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
    name = StringField("Name: ", validators=[InputRequired(), alphanumeric_validator])
    item = item = RadioField(
        "Item: ",
        choices=[
            ("Shower", "Shower"),
            ("Air Conditioning", "Air Conditioning"),
            ("Lighting", "Lighting"),
            ("Laundry", "Laundry"),
            ("Cooking", "Cooking"),
        ],
        validators=[InputRequired(), tracker_item_validator],
    )
    rate = FloatField("Rate: ", validators=[InputRequired(), NumberRange(min=2, max=4)])
    action = StringField("action", validators=[InputRequired(), alphanumeric_validator])
    old_name = StringField("old name", validators=[alphanumeric_validator])
    old_item = StringField("old item", validators=[alphanumeric_validator])


class TrackerRecordEdit(FlaskForm):
    name = StringField("Name: ", validators=[InputRequired()])
    item = StringField("Item: ", validators=[InputRequired()])
    starttime = StringField(
        "Start Time: ", validators=[InputRequired(), datetime_validator]
    )
    newendtime = StringField(
        "New End Time: ", validators=[InputRequired(), datetime_validator]
    )


class GenerateApiKeyForm(FlaskForm):
    generate_key = SubmitField("Generate API Key")


class QuestionForm(FlaskForm):
    question_one = StringField("Question 1: What is name of your mother's pre-school?")
    question_two = StringField("Question 2: What is the nickname you had?")
    question_three = StringField(
        "Question 3: What your favorite food to eat during winter?"
    )
    submit = SubmitField("Submit")
