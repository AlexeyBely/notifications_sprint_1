from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging

from core.config import settings


logger = logging.getLogger('')


class SendGrid():
    """Send email from SendGrid."""

    def __init__(self):
        self.from_email = settings.notify_from_mail

    def send_email(self, to_email: str, subject: str, content: str) -> bool:
        """Send email. Return true when a successful result."""
        message = Mail(
            from_email = self.from_email,
            to_emails = to_email,
            subject = subject,
            html_content = content
        )
        try:
            sg = SendGridAPIClient(settings.sendgrid_api_key)
            response = sg.send(message)
            logger.info(f'status_code {response.status_code}')
            logger.info(f'body {response.body}')
            logger.info(f'headers {response.headers}')
            return True
        except Exception as e:
            logger.info(f'Exception {str(e)}')
            return False
        

sendgrid_sender = SendGrid()


def get_sendgrid():
    return sendgrid_sender
            