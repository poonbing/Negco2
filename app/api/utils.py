import jwt
import datetime
from jwcrypto import jwk, jwe
from config import Config

public_key_pem = "your_public_key_pem"
private_key_pem = "your_private_key_pem"


def create_token(username):
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow(),
        "sub": username,
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


def encrypt_data(data):
    public_key = jwk.JWK.from_pem(public_key_pem)

    jwe_instance = jwe.JWE(data.encode("utf-8"))

    jwe_instance.add_recipient(public_key)

    return jwe_instance.serialize()


def decrypt_data(jwe_data):
    private_key = jwk.JWK.from_pem(private_key_pem)

    jwe_instance = jwe.JWE()

    try:
        jwe_instance.deserialize(jwe_data)
        decrypted_data = jwe_instance.decrypt(private_key)
        return decrypted_data.decode("utf-8")
    except jwe.InvalidJWEOperation:
        return "Failed JWE operation."
    except jwe.InvalidJWEData:
        return "Invalid JWE data."
