from flask import Blueprint, request, jsonify
from DB.redis_operations import get_cache

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/auth/verify-cookie", methods=["GET"])
def verify_cookie():
    token = request.cookies.get("verify_token")
    if not token or not get_cache(f"cookie:{token}"):
        return jsonify({"success": False}), 403
    return jsonify({"success": True}), 200
