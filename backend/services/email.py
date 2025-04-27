import smtplib, secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.configure import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASS,
    BASE_URL,
)
from utils.utils import red, green, reset, setup_logger


def send_email(to_address, subject, body, is_html=False):
    logger = setup_logger(__name__)
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = to_address
        msg["Subject"] = subject

        content_type = "html" if is_html else "plain"
        msg.attach(MIMEText(body, content_type))

        # Connect to SMTP server
        with smtplib.SMTP(SMTP_HOST, int(SMTP_PORT)) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        logger.info(green + f"Email sent to {to_address}" + reset)
        return True

    except smtplib.SMTPAuthenticationError:
        logger.error(
            red + "Authentication failed. Check SMTP_USER and SMTP_PASS." + reset
        )
    except smtplib.SMTPConnectError:
        logger.error(red + "Connection to SMTP server failed." + reset)
    except Exception as e:
        logger.error(red + f"Failed to send email: {e}" + reset)

    return False


def send_verification_email(email, token):
    logger = setup_logger(__name__)
    try:
        verification_url = f"{BASE_URL}/verify-email?token={token}"

        subject = "Verify Your Email"
        body = f"""
        <html>
            <body>
                <p>Welcome!</p>
                <p>Click the link below to verify your email:</p>
                <a href="{verification_url}">Verify Email</a>
                <p>This link will expire in 5 minutes.</p>
            </body>
        </html>
        """

        sent = send_email(email, subject, body, is_html=True)
        if not sent:
            return {"success": False, "message": "Failed to send verification email."}

        logger.info(green + f"Verification email sent to {email}" + reset)
        return {"success": True, "message": "Verification email sent successfully."}

    except Exception as e:
        logger.error(red + f"Error sending verification email: {e}" + reset)
        return {
            "success": False,
            "message": f"Unexpected error sending verification email: {e}",
        }


def send_2fa_code(email):
    logger = setup_logger(__name__)
    try:
        code = secrets.randbelow(900000) + 100000

        subject = "Your Two-Factor Authentication Code"
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <p>Hello,</p>
                <p>Your <strong>2FA code</strong> is:</p>
                <h2>{code}</h2>
                <p>This code will expire in 5 minutes. </p>
                <br>
                <p style="font-size: 0.9em; color: #888;">If you did not request this, please ignore this message.</p>
            </body>
        </html>
        """

        sent = send_email(email, subject, body, is_html=True)
        if not sent:
            logger.error(red + f"Failed to send 2FA email to {email}" + reset)
            return None

        logger.info(green + f"2FA code sent to {email}" + reset)
        return str(code)

    except Exception as e:
        logger.error(red + f"Error generating/sending 2FA code: {e}" + reset)
        return None
