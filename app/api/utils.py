import jwt
import datetime
from config import Config


def create_token(user_id):
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow(),
        "sub": user_id,
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return "Token has expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."
