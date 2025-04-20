from services.email import send_verification_email
from flask import Blueprint, jsonify, request, make_response
from DB.redis_operations import set_cache, get_cache, delete_cache
from DB.sql_operations import (
    insert_record,
    update_records,
    fetch_records,
    delete_records,
)
from utils.utils import (
    generate_verification_token,
    hash_password,
    setup_logger,
)

register_bp = Blueprint("register", __name__)


@register_bp.route("/api/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"success": False, "message": "All fields are required."}), 400
    if len(password) < 6:
        return (
            jsonify(
                {"success": False, "message": "Password must be at least 6 characters."}
            ),
            400,
        )

    # Check if user already exists
    existing_user = fetch_records("users", "*", "email = %s", [email])
    if existing_user:
        return jsonify({"success": False, "message": "Email already registered."}), 400

    # Hash + Token + Redis
    hashed_pw = hash_password(password)
    token = generate_verification_token()

    set_cache(f"verify_token:{token}", email, expire=300)
    set_cache(f"verify_email:{email}", token, expire=300)

    insert_success = insert_record(
        table_name="users",
        columns=["name", "email", "password"],
        values=(name, email, hashed_pw),
    )

    if not insert_success:
        return jsonify({"success": False, "message": "Registration failed."}), 500

    # Send email with token
    email_status = send_verification_email(email, token)
    if not email_status["success"]:
        return jsonify({"success": False, "message": "Email sending failed."}), 500

    # Set cookie for verify-gate
    response = jsonify(
        {
            "success": True,
            "message": "Registered successfully. Please check your email to verify.",
        }
    )
    response.set_cookie(
        key="reg_session_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=300,
    )

    return response


@register_bp.route("/api/verify-check", methods=["POST"])
def verify_check():
    data = request.json
    email = data.get("email")
    token = data.get("token")

    cookie_token = request.cookies.get("reg_session_token")

    # Check that the cookie matches the posted token
    if not cookie_token or cookie_token != token:
        delete_records("users", "email = %s", [email])
        delete_cache(f"verify_email:{email}")
        delete_cache(f"verify_token:{token}")
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Session invalid or expired. Please register again.",
                }
            ),
            403,
        )

    # Validate Redis mapping (bonus security)
    cached_email = get_cache(f"verify_token:{token}")
    if cached_email != email:
        return (
            jsonify({"success": False, "message": "Token does not match email."}),
            403,
        )

    return jsonify({"success": True, "message": "Session is valid."}), 200
