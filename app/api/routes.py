from flask import jsonify
from app.api import bp


@bp.route("/api/test", methods=["GET"])
def test_api():
    data = {
        "message": "This is a test API endpoint",
        "status": "success",
        "data": {"key1": "value1", "key2": "value2"},
    }
    return jsonify(data)
