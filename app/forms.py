from wtforms.validators import InputRequired, Email, Length, EqualTo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField


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
