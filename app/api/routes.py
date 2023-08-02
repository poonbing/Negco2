from flask import jsonify, request
from app.api import bp
from ..models import User, Report
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


@bp.route("/token", methods=["POST"])
def get_token():
    data = request.get_json()
    username = data.get("username")
    api_key = data.get("api_key")

    if not username or not api_key:
        return jsonify({"message": "Username or password is missing"}), 400

    if api_key != "admin1234":
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200


@bp.route("/user_info", methods=["GET"])
@jwt_required()
def get_user_data():
    username = get_jwt_identity()
    print(username)
    user = User.query.filter_by(username=username).first()

    if user:
        user_data = Report.query.filter_by(
            item_name="total", related_user=user.id
        ).first()

    if user_data:
        return jsonify({"user_data": user_data})
    else:
        return jsonify({"message": "User data not found"}), 404
