from config.components.env_setting import env_settings

# Celery Configuration Options
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = env_settings.admin_timezone
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = env_settings.scheduler_task_transport_timeout
CELERY_BROKER_URL = env_settings.scheduler_broker
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'visibility_timeout': env_settings.scheduler_task_transport_timeout
}
CELERY_RESULT_BACKEND = env_settings.scheduler_broker
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
