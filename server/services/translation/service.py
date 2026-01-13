from services.translation.pipelines import (
    darija_to_english,
    darija_to_language,
    english_to_darija,
    language_to_darija,
)


def translate_text(*, source_language: str, target_language: str, text: str):
    if source_language == target_language:
        return text

    if source_language == "ary":
        return (
            darija_to_english(text)
            if target_language == "en"
            else darija_to_language(text, target_language)
        )

    if target_language == "ary":
        return (
            english_to_darija(text)
            if source_language == "en"
            else language_to_darija(text, source_language)
        )

    raise ValueError(f"Unsupported translation: {source_language} → {target_language}")
