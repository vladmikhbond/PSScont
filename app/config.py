from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    token_lifetime: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# створюємо один глобальний екземпляр
settings = Settings()
