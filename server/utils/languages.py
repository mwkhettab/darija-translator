from typing import Final, Literal

LANGUAGES: Final[dict[str, dict[str, str]]] = {
    "ary": {"en": "Darija", "fr": "Darija", "ar": "الدارجة"},
    "eng": {"en": "English", "fr": "Anglais", "ar": "الإنجليزية"},
    "fra": {"en": "French", "fr": "Français", "ar": "الفرنسية"},
    "arb": {"en": "Arabic", "fr": "Arabe", "ar": "العربية"},
    "spa": {"en": "Spanish", "fr": "Espagnol", "ar": "الإسبانية"},
    "deu": {"en": "German", "fr": "Allemand", "ar": "الألمانية"},
    "ita": {"en": "Italian", "fr": "Italien", "ar": "الإيطالية"},
    "por": {"en": "Portuguese", "fr": "Portugais", "ar": "البرتغالية"},
    "rus": {"en": "Russian", "fr": "Russe", "ar": "الروسية"},
    "zho": {"en": "Chinese (Simplified)", "fr": "Chinois", "ar": "الصينية"},
    "jpn": {"en": "Japanese", "fr": "Japonais", "ar": "اليابانية"},
    "kor": {"en": "Korean", "fr": "Coréen", "ar": "الكورية"},
    "hin": {"en": "Hindi", "fr": "Hindi", "ar": "الهندية"},
    "ind": {"en": "Indonesian", "fr": "Indonésien", "ar": "الإندونيسية"},
    "vie": {"en": "Vietnamese", "fr": "Vietnamien", "ar": "الفيتنامية"},
    "tur": {"en": "Turkish", "fr": "Turc", "ar": "التركية"},
    "dut": {"en": "Dutch", "fr": "Néerlandais", "ar": "الهولندية"},
    "pol": {"en": "Polish", "fr": "Polonais", "ar": "البولندية"},
    "ukr": {"en": "Ukrainian", "fr": "Ukrainien", "ar": "الأوكرانية"},
    "heb": {"en": "Hebrew", "fr": "Hébreu", "ar": "العبرية"},
    "urd": {"en": "Urdu", "fr": "Ourdou", "ar": "الأردية"},
    "tam": {"en": "Tamil", "fr": "Tamoul", "ar": "التاميلية"},
    "tha": {"en": "Thai", "fr": "Thaï", "ar": "التايلاندية"},
    "swh": {"en": "Swahili", "fr": "Swahili", "ar": "السواحيلية"},
}


def is_supported_language(lang_code: str) -> bool:
    return lang_code in LANGUAGES


def get_language_name(
    lang_code: str,
    display_lang: Literal["en", "fr", "ar"] = "en",
) -> str | None:
    return LANGUAGES.get(lang_code, {}).get(display_lang)


def get_supported_languages() -> dict[str, dict[str, str]]:
    return LANGUAGES
