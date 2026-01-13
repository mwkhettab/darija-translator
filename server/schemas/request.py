from pydantic import BaseModel, Field


class TranslateRequest(BaseModel):
    text: str = Field(max_length=100)
    source_language: str = Field(max_length=3)
    target_language: str = Field(max_length=3)