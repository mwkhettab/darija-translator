from pydantic import BaseModel
from typing import Literal

class ScriptText(BaseModel):
    script: Literal["latin", "arabic"]
    text: str

class TranslateSingleTextResponse(BaseModel):
    language: str
    text: str

class TranslateMultiTextResponse(BaseModel):
    language: str
    variants: list[ScriptText]