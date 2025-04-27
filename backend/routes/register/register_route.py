import re
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


FIELD_RULES = {
    "name": {
        "required": True,
        "sanitize": lambda value: re.sub(r"[^A-Za-z0-9 _-]", "", value),
    },
    "email": {
        "required": True,
        "sanitize": lambda value: value.strip(),
        "validate": lambda value: re.fullmatch(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", value
        )
        is not None,
        "error_message": "Invalid email format.",
    },
    "password": {
        "required": True,
        "sanitize": lambda value: re.sub(r'[<>"\'`;]', "", value),
        "validate": lambda value: len(value) >= 6,
        "error_message": "Password must be at least 6 characters.",
    },
}


@register_bp.route("/api/register", methods=["POST"])
def register():
    data = request.json
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

        sanitize_fn = rules.get("sanitize")
        if sanitize_fn:
            value = sanitize_fn(value)

        validate_fn = rules.get("validate")
        if validate_fn and not validate_fn(value):
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

    data = sanitized_data

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    existing_user = fetch_records(
        table_name="users", where_clause="email = %s", params=(email,)
    )

    if existing_user:
        return (
            jsonify({"success": False, "message": "Email is already registered."}),
            400,
        )

    password = hash_password(password)

    user_id = insert_record(
        table_name="users",
        columns=["name", "email", "password"],
        values=(name, email, password),
    )

    if user_id:
        return jsonify({"success": True, "message": "User pending!"}), 200
    else:
        return (
            jsonify(
                {"success": False, "message": "An error occurred while registering."}
            ),
            500,
        )
