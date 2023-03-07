import os
import logging
from jinja2 import Environment, FileSystemLoader

from app_celery import app
from email_services.sendgrid import get_sendgrid
from email_services.email_service_abc import BaseServiceEmail
from email_services.mailhog import get_mailhog
from core.config import settings


logger = logging.getLogger('')


@app.task
def send_email(template_name: str, vars: dict):
    """Sending an email."""
    path = os.path.dirname(__file__)
    path = os.path.dirname(path)
    env = Environment(loader=FileSystemLoader(f'{path}/templates'))
    template = env.get_template(f'{template_name}')
    output = template.render(**vars)
    if settings.mailhog_enable is not True:
        service_email = get_sendgrid()
    else:
        service_email = get_mailhog()
    result = service_email.send_email(
        to_email=vars['user_email'],
        subject='news from movies service',
        content=output  
    )    
    logger.info(f'result {result}')
