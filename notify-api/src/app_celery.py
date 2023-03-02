from celery import Celery
from core.config import settings

url_broker = 'amqp://{0}:{1}@{2}:{3}/{4}'.format(
    settings.rabbitmq_default_user,
    settings.rabbitmq_default_pass,
    settings.notify_rabbitmq_host,
    settings.notify_rabbitmq_port,
    settings.rabbitmq_default_vhost,
)

app = Celery('notify', broker=url_broker, include=['tasks.email'])