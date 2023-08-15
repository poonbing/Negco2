from ..extensions import mail
from flask_mail import Message
from random import randint
from flask import render_template
from datetime import datetime, timedelta

access_codes = {}


def generate_access_code():
    access_code = randint(100000, 999999)
    expiration_time = datetime.now() + timedelta(minutes=15)
    return access_code, expiration_time


def send_recovery_email(email, access_code):
    msg = Message("Password Recovery", recipients=[email])
    msg.html = render_template("recovery/emailTemplate.html", access_code=access_code)
    mail.send(msg)
