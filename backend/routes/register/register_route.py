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
