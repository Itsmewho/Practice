from flask import Blueprint, request, jsonify, json
from DB.redis_operations import get_cache, set_cache, delete_cache
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

    raw = get_cache(f"session:{token}")
    if not raw:
        response = jsonify({"success": False})
        response.delete_cookie("session_token")
        return response, 403

    session_data = json.loads(raw)
    expected_ip = session_data.get("ip")
    expected_ua = session_data.get("user_agent")

    current_ip = request.remote_addr
    current_ua = request.headers.get("User-Agent", "")

    if expected_ip != current_ip or expected_ua != current_ua:
        delete_cache(f"session:{token}")
        response = jsonify(
            {
                "success": False,
                "message": "Session environment mismatch. You have been logged out.",
            }
        )
        response.delete_cookie("session_token")
        return response, 403

    # Refresh session TTL
    set_cache(f"session:{token}", raw, expire=SESSION_EXPIRE_SECONDS)

    response = jsonify({"success": True})
    response.set_cookie(
        key="session_token",
        value=token,
        max_age=SESSION_EXPIRE_SECONDS,
        httponly=True,
        samesite="Strict",
        secure=HTTPONLY,
    )
    return response, 200
