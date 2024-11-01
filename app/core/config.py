from pydantic import BaseModel
from pydantic_settings import BaseSettings
from functools import lru_cache


class DatabaseSettings(BaseModel):
    host: str
    port: int
    user: str
    password: str
    db: str


class Settings(BaseSettings):
    # Настройки проекта FasAPI
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "FastAPI skeletor"
    version: str = "1.0.0"

    db: DatabaseSettings

    @property
    def fastapi_settings(self) -> dict[str, ...]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
