import json
from flask import Blueprint, request, jsonify
from DB.sql_operations import fetch_records
from config.configure import HTTPONLY
from DB.redis_operations import get_cache, set_cache, delete_cache
from utils.utils import (
    verify_password,
    generate_six_digit_code,
    generate_verification_token,
    setup_logger,
    LOGIN_RULES,
)
from services.email import send_2fa_code

login_bp = Blueprint("login", __name__)
logger = setup_logger(__name__)


@login_bp.route("/api/login", methods=["POST"])
def login():
    data = request.json
    user_ip = request.remote_addr
    user_agent = request.headers.get("User-Agent", "")
    ip_key = f"login_attempts:{user_ip}"

    attempts = get_cache(ip_key)
    if attempts and int(attempts) >= 3:
        return (
            jsonify({"success": False, "message": "Too many attempts. Please wait."}),
            429,
        )
    set_cache(ip_key, (int(attempts) if attempts else 0) + 1, expire=60)

    sanitized = {}
    for field, rules in LOGIN_RULES.items():
        value = data.get(field, "")
        if rules.get("required") and not value:
            return jsonify({"success": False, "message": f"{field} is required"}), 400
        if sanitize_fn := rules.get("sanitize"):
            value = sanitize_fn(value)
        if (validate_fn := rules.get("validate")) and not validate_fn(value):
            return (
                jsonify({"success": False, "message": rules.get("error_message")}),
                400,
            )
        sanitized[field] = value

    email = sanitized["email"]
    password = sanitized["password"]

    records = fetch_records(
        table_name="users",
        where_clause="email = %s AND is_verified = TRUE",
        params=(email,),
    )
    if not records:
        return jsonify({"success": False, "message": "Invalid credentials."}), 403

    user = records[0]
    hashed_password = user.get("password")
    verified = verify_password(password, hashed_password)
    if not verified["success"]:
        return jsonify({"success": False, "message": verified["message"]}), 403

    throttle_key = f"login_sent:{email}:{user_ip}"
    if get_cache(throttle_key):
        return (
            jsonify(
                {
                    "success": False,
                    "message": "A login email has already been sent. Please check your inbox.",
                }
            ),
            429,
        )

    token = generate_six_digit_code()
    login_token = generate_verification_token()
    token_data = {
        "email": email,
        "ip": user_ip,
        "user_agent": user_agent,
        "user_id": user.get("id"),
    }
    set_cache(f"cookie:{login_token}", json.dumps(token_data), expire=300)
    set_cache(f"2fa:{token}", json.dumps(token_data), expire=300)
    set_cache(throttle_key, "sent", expire=300)

    send_result = send_2fa_code(email, token)
    if not send_result.get("success"):
        return jsonify({"success": False, "message": "Failed to send 2FA email."}), 500

    response = jsonify({"success": True, "message": "Login link sent to your email."})

    response.set_cookie(
        key="login_cookie",
        value=login_token,
        max_age=300,
        httponly=True,
        samesite="strict",
    )
    return response, 200


@login_bp.route("/api/verify-login", methods=["POST"])
def verify_login():
    data = request.json
    code = data.get("code")

    if not code or not code.isdigit() or len(code) != 6:
        return jsonify({"success": False, "message": "Invalid or missing code."}), 400

    raw = get_cache(f"2fa:{code}")
    if not raw:
        return jsonify({"success": False, "message": "Invalid or expired code."}), 403

    token_data = json.loads(raw)
    token_ip = token_data["ip"]
    token_ua = token_data["user_agent"]
    token_email = token_data["email"]
    token_user_id = token_data["user_id"]

    # Match IP and User-Agent
    if (
        request.remote_addr != token_ip
        or request.headers.get("User-Agent", "") != token_ua
    ):
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Device mismatch. Please retry from the original device.",
                }
            ),
            403,
        )

    user = fetch_records("users", where_clause="id = %s", params=(token_user_id,))
    if not user:
        return jsonify({"success": False, "message": "User no longer exists."}), 404

    session_token = generate_verification_token()
    set_cache(
        f"session:{session_token}",
        json.dumps(
            {
                "user_id": token_user_id,
                "email": token_email,
                "ip": token_ip,
                "user_agent": token_ua,
            }
        ),
        expire=3600,
    )

    delete_cache(f"2fa:{code}")
    delete_cache(f"login_sent:{token_email}:{token_ip}")

    response = jsonify({"success": True, "message": "Login successful."})
    response.set_cookie(
        key="session_token",
        value=session_token,
        max_age=3600,
        httponly=True,
        samesite="Lax",
        secure=HTTPONLY,
    )
    return response, 200
