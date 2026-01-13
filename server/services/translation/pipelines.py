from services.translation.hf_client import (
    translate_darija_to_english,
    translate_english_to_darija,
)
from services.translation.openai_client import translate
from services.translation.transliteration import transliterate_darija
from utils.languages import is_supported_language


def _check_supported_language(lang_code: str):
    if not is_supported_language(lang_code):
        raise ValueError(f"Unsupported language code: {lang_code}")


def darija_to_language(text: str, target_language: str) -> dict:
    _check_supported_language(target_language)

    darija_arabic = transliterate_darija(text, direction="to_arabic")

    english = translate_darija_to_english(darija_arabic)

    translation = translate(
        source_language="ary",
        target_language=target_language,
        source_text=darija_arabic,
        english_reference=english,
    )

    return {"language": target_language, "text": translation}


def language_to_darija(text: str, source_language: str) -> dict:
    _check_supported_language(source_language)

    english = translate(
        source_language=source_language,
        target_language="en",
        source_text=text,
    )

    darija_arabic = translate_english_to_darija(english)

    darija_latin = transliterate_darija(darija_arabic, direction="to_latin")

    return {
        "language": "ary",
        "variants": [
            {"script": "arabic", "text": darija_arabic},
            {"script": "latin", "text": darija_latin},
        ],
    }


def darija_to_english(text: str) -> dict:
    darija_arabic = transliterate_darija(text, direction="to_arabic")
    english = translate_darija_to_english(darija_arabic)

    return {"language": "en", "text": english}


def english_to_darija(text: str) -> dict:
    darija_arabic = translate_english_to_darija(text)

    darija_latin = transliterate_darija(darija_arabic, direction="to_latin")

    return {
        "language": "ary",
        "variants": [
            {"script": "arabic", "text": darija_arabic},
            {"script": "latin", "text": darija_latin},
        ],
    }
