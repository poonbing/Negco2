from flask import jsonify, request, current_app
from app.api import bp
from ..models import User, Report, APIKey, Articles
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..extensions import csrf
from app import limiter
from config import Config
from .utils import is_valid_username
from datetime import datetime
from sqlalchemy import func


@bp.route("/token", methods=["POST"])
@csrf.exempt
@limiter.limit("100/day")
def get_token():
    data = request.get_json()
    username = data.get("username")
    api_key = data.get("api_key")
    if not username or not api_key:
        current_app.logger.info(
            "Invalid Credentials",
            extra={
                "user_id": username,
                "address": request.remote_addr,
                "page": request.path,
                "category": "API",
            },
        )
        return jsonify({"message": "Username or password is missing"}), 400

    if is_valid_username(username):
        user = User.query.filter_by(username=username).first()
        if user:
            api_key_objs = APIKey.query.filter_by(user_id=user.id).all()
            for api_key_obj in api_key_objs:
                if api_key_obj.decrypt_key(Config.ENCRYPTION_KEY) == api_key:
                    access_token = create_access_token(identity=username)
                    current_app.logger.info(
                        f"API Key Created {access_token}",
                        extra={
                            "user_id": username,
                            "address": request.remote_addr,
                            "page": request.path,
                            "category": "API",
                        },
                    )
                    return jsonify({"access_token": access_token}), 200

            current_app.logger.info(
                "Invalid Credentials",
                extra={
                    "user_id": username,
                    "address": request.remote_addr,
                    "page": request.path,
                    "category": "API",
                },
            )
            return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({"message": "Invalid credentials"}), 401


@bp.route("/articles", methods=["GET"])
@limiter.limit("100/day")
def get_articles_of_the_day():
    today = datetime.today().date()
    articles = Articles.query.filter(func.DATE(Articles.date_added) == today).all()

    if not articles:
        return jsonify({"message": "No articles published today."}), 200

    serialized_articles = []
    for article in articles:
        serialized_articles.append(
            {
                "title": article.title,
                "description": article.description,
                "date_added": article.date_added,
                "writer": article.writer,
                "paragraph": article.paragraph,
                "time_ago": article.time_ago(),
            }
        )

    return jsonify(serialized_articles)


@bp.route("/user_info", methods=["GET"])
@jwt_required()
@limiter.limit("100/day")
def get_user_data():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()

    if user:
        user_data = Report.query.filter_by(
            item_name="total", related_user=user.id
        ).first()

        if user_data:
            user_data_dict = {
                "username": user.username,
                "item_name": user_data.item_name,
                "month": user_data.month,
                "year": user_data.year,
                "total_usage": user_data.total_usage,
                "energy_goals": user_data.energy_goals,
            }
            return jsonify({"user_data": user_data_dict})
    else:
        return jsonify({"message": "User data not found"}), 404
