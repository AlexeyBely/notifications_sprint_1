import os
import logging
from jinja2 import Environment, FileSystemLoader

from app_celery import app
from tasks.sendgrid import get_sendgrid, SendGrid


logger = logging.getLogger('')


@app.task
def send_email(template_name: str, vars: dict):
    """Sending an email."""
    path = os.path.dirname(__file__)
    path = os.path.dirname(path)
    env = Environment(loader=FileSystemLoader(f'{path}/templates'))
    template = env.get_template(f'{template_name}')
    output = template.render(**vars)
    logger.info(f'result {output}')
    service_email: SendGrid = get_sendgrid()
    result = service_email.send_email(
        to_email=vars['user_email'],
        subject='news from movies service',
        content=output  
    )    
    logger.info(f'result {result}')
