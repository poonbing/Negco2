from flask import jsonify, request
from app.api import bp
from ..models import User, Report
from .utils import create_token, verify_token, encrypt_data


@bp.route("/token", methods=["GET"])
def get_token():
    data = request.get_json()
    api_key = data.get("api_key")
    username = data.get("username")

    user = User.query.filter_by(username=username).first()

    if user:
        if api_key == user.api_key:
            token = create_token(username)
            return jsonify({"token": token})
        else:
            return jsonify({"message": "Invalid API key"}), 401


@bp.route("/api/users", methods=["GET"])
def get_user_data():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token is missing"}), 401

    username = verify_token(token)
    user_data = Report.query.filter_by(item_name="total", username=username).first()

    if user_data:
        encrypted_data = encrypt_data(user_data)
        return jsonify({"encrypted_data": encrypted_data})
    else:
        return jsonify({"message": "User data not found"}), 404
