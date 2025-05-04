import logging, bcrypt, secrets, re, random
from colorama import Style, Fore


reset = Style.RESET_ALL
blue = Fore.BLUE
yellow = Fore.YELLOW
red = Fore.RED
green = Fore.GREEN


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


LOGIN_RULES = {
    "email": {
        "required": True,
        "sanitize": lambda v: v.strip(),
        "validate": lambda v: re.fullmatch(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", v
        )
        is not None,
        "error_message": "Invalid email format.",
    },
    "password": {
        "required": True,
        "sanitize": lambda v: re.sub(r'[<>"\'`;]', "", v),
        "validate": lambda v: len(v) >= 6,
        "error_message": "Password must be at least 6 characters.",
    },
}


def setup_logger(name: str, level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    return logging.getLogger(name)


def generate_verification_token():
    return secrets.token_urlsafe(32)


def generate_six_digit_code():
    return f"{random.randint(100000, 999999)}"


def hash_password(password):
    logger = setup_logger("hash_password")
    try:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        logger.info(green + "Password hashed successfully." + reset)
        return hashed.decode("utf-8")
    except Exception as e:
        logger.error(red + f"Password hashing failed: {e}" + reset)
        return None


def verify_password(plain_password, hashed_password):
    # Return instead of logger as it can be used to inform the user.
    try:
        result = bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
        if result:
            return {"success": True, "message": "Password verified successfully."}
        else:
            return {"success": False, "message": "Password does not match."}

    except Exception as e:
        return {"success": False, "message": f"Error verifying password: {str(e)}"}
