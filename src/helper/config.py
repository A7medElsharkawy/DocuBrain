from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    FILE_ALLOWED_TYPE: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    MONGO_URI: str
    MONGO_DATABASE: str


    class Config:
        env_file = ".env"

def get_settings():
    return Setting()