import logging, bcrypt, secrets
from colorama import Style, Fore


reset = Style.RESET_ALL
blue = Fore.BLUE
yellow = Fore.YELLOW
red = Fore.RED
green = Fore.GREEN


def setup_logger(name: str, level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    return logging.getLogger(name)


def generate_verification_token():
    return secrets.token_urlsafe(32)


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
