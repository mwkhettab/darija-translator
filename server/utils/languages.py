from typing import Final, Literal

LANGUAGES: Final[dict[str, dict[str, str]]] = {
    "ary": {"code": "ary_Arab", "en": "Darija", "fr": "Darija", "ar": "الدارجة"},
    "en": {"code": "eng_Latn", "en": "English", "fr": "Anglais", "ar": "الإنجليزية"},
    "fra": {"code": "fra_Latn", "en": "French", "fr": "Français", "ar": "الفرنسية"},
    "arb": {"code": "arb_Arab", "en": "Arabic", "fr": "Arabe", "ar": "العربية"},
    "spa": {"code": "spa_Latn", "en": "Spanish", "fr": "Espagnol", "ar": "الإسبانية"},
    "deu": {"code": "deu_Latn", "en": "German", "fr": "Allemand", "ar": "الألمانية"},
    "ita": {"code": "ita_Latn", "en": "Italian", "fr": "Italien", "ar": "الإيطالية"},
    "por": {
        "code": "por_Latn",
        "en": "Portuguese",
        "fr": "Portugais",
        "ar": "البرتغالية",
    },
    "rus": {"code": "rus_Cyrl", "en": "Russian", "fr": "Russe", "ar": "الروسية"},
    "zho": {
        "code": "zho_Hans",
        "en": "Chinese (Simplified)",
        "fr": "Chinois",
        "ar": "الصينية",
    },
    "jpn": {"code": "jpn_Jpan", "en": "Japanese", "fr": "Japonais", "ar": "اليابانية"},
    "kor": {"code": "kor_Hang", "en": "Korean", "fr": "Coréen", "ar": "الكورية"},
    "hin": {"code": "hin_Deva", "en": "Hindi", "fr": "Hindi", "ar": "الهندية"},
    "ind": {
        "code": "ind_Latn",
        "en": "Indonesian",
        "fr": "Indonésien",
        "ar": "الإندونيسية",
    },
    "vie": {
        "code": "vie_Latn",
        "en": "Vietnamese",
        "fr": "Vietnamien",
        "ar": "الفيتنامية",
    },
    "tur": {"code": "tur_Latn", "en": "Turkish", "fr": "Turc", "ar": "التركية"},
    "dut": {"code": "nld_Latn", "en": "Dutch", "fr": "Néerlandais", "ar": "الهولندية"},
    "pol": {"code": "pol_Latn", "en": "Polish", "fr": "Polonais", "ar": "البولندية"},
    "ukr": {
        "code": "ukr_Cyrl",
        "en": "Ukrainian",
        "fr": "Ukrainien",
        "ar": "الأوكرانية",
    },
    "heb": {"code": "heb_Hebr", "en": "Hebrew", "fr": "Hébreu", "ar": "العبرية"},
    "urd": {"code": "urd_Arab", "en": "Urdu", "fr": "Ourdou", "ar": "الأردية"},
    "tam": {"code": "tam_Taml", "en": "Tamil", "fr": "Tamoul", "ar": "التاميلية"},
    "tha": {"code": "tha_Thai", "en": "Thai", "fr": "Thaï", "ar": "التايلاندية"},
    "swh": {"code": "swh_Latn", "en": "Swahili", "fr": "Swahili", "ar": "السواحيلية"},
}


def is_supported_language(lang_code: str) -> bool:
    return lang_code in LANGUAGES


def get_language_name(
    lang_code: str,
    display_lang: Literal["en", "fr", "ar"] = "en",
) -> str | None:
    return LANGUAGES.get(lang_code, {}).get(display_lang)


def get_language_code(lang_code: str) -> str | None:
    return LANGUAGES.get(lang_code, {}).get("code")


def get_supported_languages() -> dict[str, dict[str, str]]:
    return {
        lang_code: {k: v for k, v in details.items() if k != "code"}
        for lang_code, details in LANGUAGES.items()
    }
