# Python Modules
from flask import redirect, url_for
from flask_login import current_user
from functools import wraps
from PIL import Image
from io import BytesIO


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


def resize(
    image_input, width=None, height=None, antialias=True, keep_aspect_ratio=True
):
    if isinstance(image_input, str):
        with open(image_input, "rb") as file:
            image_bytes = file.read()
    elif isinstance(image_input, bytes):
        image_bytes = image_input
    else:
        raise ValueError(
            "Invalid image_input type. It should be either a file path (str) or image bytes (bytes)."
        )

    if width is None and height is None:
        raise ValueError("Either width or height must be provided.")
    if not keep_aspect_ratio and (width is None or height is None):
        raise ValueError(
            "Both width and height must be provided when keep_aspect_ratio is False."
        )

    foo = Image.open(BytesIO(image_bytes))

    if keep_aspect_ratio:
        original_width, original_height = foo.size
        if width is None:
            width = int(height * original_width / original_height)
        elif height is None:
            height = int(width * original_height / original_width)

    if antialias:
        foo = foo.resize((width, height), Image.ANTIALIAS)
    else:
        foo = foo.resize((width, height))

    output_bytes = BytesIO()
    foo.save(output_bytes, format="JPEG")
    return output_bytes.getvalue()
