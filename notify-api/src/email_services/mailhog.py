import logging
import smtplib
from smtplib import SMTPException

from core.config import settings
from email_services.email_service_abc import BaseServiceEmail


logger = logging.getLogger('')


class MailHog(BaseServiceEmail):
    """Send email to MailHog."""

    def __init__(self):
        self.from_email = settings.notify_from_mail

    def send_email(self, to_email: str, subject: str, content: str) -> bool:
        """Send email. Return true when a successful result."""
        message = f'From: <{self.from_email}>'
        message += f'\nTo: <{to_email}>'
        message += f'\nSubject: {subject}\n'
        message += f'\n{content}'
        receivers = [to_email, ]
        try:
            smtp_client = smtplib.SMTP(
                host=settings.mailhog_host,
                port=settings.mailhog_port        
            )
            smtp_client.sendmail(self.from_email, receivers, message)
            return True         
        except SMTPException:
            logger.info('Error: unable to send email')
            return False        
        

mailhog_sender = MailHog()


def get_mailhog():
    return mailhog_sender
