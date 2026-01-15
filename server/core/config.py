from pydantic_settings import BaseSettings
from pydantic import AnyUrl


class Settings(BaseSettings):
    openai_api_key: str
    redis_url: AnyUrl
    cors_allowed_origins: str
    d2e_model_id: str = "mwkhettab/nllb-200-darjia-en"
    e2d_model_id: str = "mwkhettab/nllb-200-en-darija"
    translation_model_id: str = "facebook/nllb-200-distilled-600M"
    transliteration_model_id: str = "atlasia/Transliteration-Moroccan-Darija"
    environment: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
