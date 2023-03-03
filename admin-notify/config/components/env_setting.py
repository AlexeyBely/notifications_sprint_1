from pydantic import BaseSettings, Field, root_validator


class EnvSettings(BaseSettings):
    secret_key: str = Field('django-insecure-', env='notify_dj_secret_key')
    debug: bool = Field(True, env='notify_debug')
    static: str = Field('notify_static', env='notify_static')
    media: str = Field('notify_media', env='notify_media')
    psql_name: str = Field('modify_database', env='notify_postgres_db')
    psql_user: str = Field('app', env='notify_postgres_name')
    psql_password: str = Field('123qwe', env='notify_postgres_password')
    psql_port: int = Field(5432, env='notify_postgres_port')
    psql_host: str = Field('127.0.0.1', env='notify_postgres_host')
    admin_timezone: str = 'Europe/Moscow'
    scheduler_task_transport_timeout: int = 3600
    scheduler_broker_redis_host: str = '127.0.0.1'
    scheduler_broker_redis_port: int = 6379
    scheduler_broker: str | None = None
    schedule_delay_min: int = 1
    notify_api_port: int = 8001
    notify_api_host: str = '127.0.0.1'
    notify_api_url: str = 'http://127.0.0.1:8001/notify/api/v1/task/'
    notify_api_timeout: int = 5

    @root_validator
    def compute_service_url(cls, values):
        if values.get('scheduler_broker', None) is None:
            port = values['scheduler_broker_redis_port']
            host = values['scheduler_broker_redis_host']
            values['scheduler_broker'] = f'redis://{host}:{port}/0'
        if values.get('notify_api_url', None) is None:
            port = values['notify_api_port']
            host = values['notify_api_host']
            values['notify_api_url'] = f'http://{host}:{port}/notify/api/v1/task/'
        return values    


env_settings = EnvSettings()
