import smtplib, secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.configure import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS
from utils.utils import red, green, reset, setup_logger

logger = setup_logger(__name__)


def send_email(to_address, subject, body, is_html=False):
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


def send_2fa_code(email):
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
