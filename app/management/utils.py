# Python Modules
from flask import redirect, url_for
from flask_login import current_user
from functools import wraps
from PIL import Image
from io import BytesIO
import re
import string
import secrets


def generate_api_key(length=60):
    alphabet = string.ascii_letters + string.digits
    api_key = "".join(secrets.choice(alphabet) for _ in range(length))
    return api_key


def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(
                required_role
            ):
                return redirect(url_for("management.dashboard"))
            return func(*args, **kwargs)

        return decorated_view

    return decorator


def compress_and_resize(image_bytes, max_size=(300, 300), quality=85):
    try:
        image = Image.open(BytesIO(image_bytes))

        image.thumbnail(max_size)

        compressed_image_buffer = BytesIO()

        image.save(compressed_image_buffer, format=image.format, quality=quality)

        compressed_resized_image_bytes = compressed_image_buffer.getvalue()

        return compressed_resized_image_bytes
    except Exception as e:
        print("Error:", e)
        return None
