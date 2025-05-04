import json
from config.configure import HTTPONLY
from services.email import send_verification_email
from flask import Blueprint, jsonify, request
from DB.redis_operations import set_cache, get_cache, delete_cache
from DB.sql_operations import (
    insert_record,
    fetch_records,
)
from utils.utils import generate_verification_token, hash_password, FIELD_RULES

register_bp = Blueprint("register", __name__)


@register_bp.route("/api/register", methods=["POST"])
def register():
    data = request.json
    user_ip = request.remote_addr
    user_agent = request.headers.get("User-Agent", "")
    ip_key = f"register_attempts:{user_ip}"

    attempts = get_cache(ip_key)
    if attempts and int(attempts) >= 3:
        return (
            jsonify({"success": False, "message": "Too many attempts. Please wait."}),
            429,
        )
    set_cache(ip_key, (int(attempts) if attempts else 0) + 1, expire=60)

    sanitized_data = {}
    for field, rules in FIELD_RULES.items():
        value = data.get(field, "")
        if rules.get("required") and not value:
            return (
                jsonify(
                    {"success": False, "message": f"{field.capitalize()} is required."}
                ),
                400,
            )
        if sanitize_fn := rules.get("sanitize"):
            value = sanitize_fn(value)
        if (validate_fn := rules.get("validate")) and not validate_fn(value):
            return (
                jsonify(
                    {
                        "success": False,
                        "message": rules.get("error_message", "Invalid input."),
                    }
                ),
                400,
            )
        sanitized_data[field] = value

    email = sanitized_data["email"]
    if fetch_records("users", where_clause="email = %s", params=(email,)):
        return (
            jsonify({"success": False, "message": "Email is already registered."}),
            400,
        )

    sanitized_data["password"] = hash_password(sanitized_data["password"])
    sanitized_data["ip"] = user_ip
    sanitized_data["user_agent"] = user_agent

    token = generate_verification_token()
    set_cache(f"verify:{token}", json.dumps(sanitized_data), expire=300)

    cookie_token = generate_verification_token()
    set_cache(f"cookie:{cookie_token}", "valid", expire=300)

    result = send_verification_email(email, token)
    if not result.get("success"):
        return (
            jsonify(
                {"success": False, "message": "Failed to send verification email."}
            ),
            500,
        )

    response = jsonify({"success": True, "message": "Verification email sent!"})
    response.set_cookie(
        key="verify_token",
        value=cookie_token,
        max_age=300,
        httponly=True,
        samesite="Lax",
        secure=HTTPONLY,
    )
    return response, 200


@register_bp.route("/api/verify-email", methods=["GET"])
def verify_email():
    token = request.args.get("token")
    if not token:
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Missing token.",
                    "redirectImmediately": True,
                }
            ),
            400,
        )

    raw = get_cache(f"verify:{token}")
    if not raw:
        return jsonify({"success": False, "message": "Invalid or expired token."}), 400

    token_data = json.loads(raw)
    if (
        request.remote_addr != token_data["ip"]
        or request.headers.get("User-Agent", "") != token_data["user_agent"]
    ):
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Device mismatch. Use your original device.",
                }
            ),
            403,
        )

    try:
        insert_record(
            table_name="users",
            columns=["name", "email", "password", "is_verified"],
            values=(
                token_data["name"],
                token_data["email"],
                token_data["password"],
                True,
            ),
        )
        delete_cache(f"verify:{token}")
        return (
            jsonify(
                {"success": True, "message": "Email verified and account created!"}
            ),
            200,
        )
    except Exception:
        return (
            jsonify({"success": False, "message": "Failed to complete registration."}),
            500,
        )
