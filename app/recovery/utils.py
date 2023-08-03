from ..extensions import mail
from flask_mail import Message
from random import randint
from flask import render_template

access_codes = {}


def generate_access_code():
    return randint(100000, 999999)


def send_recovery_email(email, access_code):
    msg = Message("Password Recovery", recipients=[email])
    msg.html = render_template("recovery/emailTemplate.html", access_code=access_code)
    mail.send(msg)
