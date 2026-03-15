from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    FILE_ALLOWED_TYPE: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    MONGO_URI: str
    MONGO_DATABASE: str
    GERNERATION_BACKEND : str
    EMBEDDING_BACKEND :str
    
    OPENAI_API_KEY :str = None
    OPEN_AI_URL :str= None
    COHERE_API_KEY :str= None

    GENERATION_MODEL_ID :str= None
    EMBEDDDING_MODEL_ID :str= None
    EMBEDDDING_MODEL_SIZE :int= None

    INPUT_DAFAULT_MAX_CHARACTERS :int= None
    GENERATION_DEFAULT_MAX_TOKENS :int= None
    GENERATION_DEFAULT_TEMPERATURE :float= None

    VECTORE_DB_BACKEND : str = None
    VECTORE_DB_PATH :str = None
    VECTORE_DB_DISTANCE :str = None

    class Config:
        env_file = ".env"

def get_settings():
    return Setting()