from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    app_title: str = 'Вопросы для викторины'
    database_dsn: PostgresDsn

    class Config:
        env_file = '.env'


settings = Settings()
