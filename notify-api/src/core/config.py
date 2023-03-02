from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field


logging_config.dictConfig(LOGGING)


class ApiSettings(BaseSettings):
    project_name: str = 'Notification'    
    psql_name: str = Field('modify_database', env='notify_postgres_db')
    psql_user: str = Field('app', env='notify_postgres_name')
    psql_password: str = Field('123qwe', env='notify_postgres_password')
    psql_port: int = Field(5432, env='notify_postgres_port')
    psql_host: str = Field('127.0.0.1', env='notify_postgres_host')
    access_token_secret_key: str = '256-bit-secret-key-1'
    token_algoritm: str = 'HS256'
    max_page_size: int = 100
    auth_users_url: str = 'http://127.0.0.1:5000/auth/users/'
    auth_login_url: str = 'http://127.0.0.1:5000/auth/login/'
    auth_login_email: str = 'superuser@ex.com'
    auth_login_password: str = 'superUserSuperPassword'
    api_films_url: str = 'http://127.0.0.1:9000/api/v1/films/'
    rabbitmq_default_user: str
    rabbitmq_default_pass: str
    rabbitmq_default_vhost: str
    notify_rabbitmq_host: str
    notify_rabbitmq_port: int
    sendgrid_api_key: str
    notify_from_mail: str


settings = ApiSettings()
