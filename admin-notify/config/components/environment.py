from pydantic import BaseSettings, Field


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


env_settings = EnvSettings()