import bleach
import re


def sanitize_input(user_input):
    sanitized_html = bleach.clean(user_input, strip=True)

    sanitized_input = re.sub(r"\.\./|\.\\", "", sanitized_html)

    return sanitized_input
