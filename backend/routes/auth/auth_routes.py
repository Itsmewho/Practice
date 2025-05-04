from flask import Blueprint, request, jsonify
from DB.redis_operations import get_cache, set_cache
from config.configure import HTTPONLY, SESSION_EXPIRE_SECONDS

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/auth/verify-cookie", methods=["GET"])
def verify_cookie():
    token = request.cookies.get("verify_token")
    if not token or not get_cache(f"cookie:{token}"):
        return jsonify({"success": False}), 403
    return jsonify({"success": True}), 200


@auth_bp.route("/api/auth/verify-login-cookie", methods=["GET"])
def verify_login_cookie():
    token = request.cookies.get("login_cookie")
    if not token or not get_cache(f"cookie:{token}"):
        return jsonify({"success": False}), 403
    return jsonify({"success": True}), 200


@auth_bp.route("/api/auth/session-check", methods=["GET"])
def session_check():
    token = request.cookies.get("session_token")
    if not token:
        return jsonify({"success": False}), 403

    data = get_cache(f"session:{token}")
    if not data:
        return jsonify({"success": False}), 403

    set_cache(f"session:{token}", data, expire=SESSION_EXPIRE_SECONDS)

    response = jsonify({"success": True})
    response.set_cookie(
        key="session_token",
        value=token,
        max_age=SESSION_EXPIRE_SECONDS,
        httponly=True,
        samesite="Lax",
        secure=HTTPONLY,
    )
    return response, 200
