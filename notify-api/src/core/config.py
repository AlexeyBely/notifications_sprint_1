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
    default_page_size: int = 20
    max_page_size: int = 100


settings = ApiSettings()
