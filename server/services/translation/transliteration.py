import re
from typing import Literal
from services.translation.openai_client import transliterate_darija_latin_to_arabic


ARABIC_PATTERN = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]")


def contains_arabic(text: str) -> bool:
    return bool(ARABIC_PATTERN.search(text))


def transliterate_darija_arabic_to_latin(text: str) -> str:

    def normalize_arabic(text: str) -> str:

        diacritics = re.compile(r"[\u064B-\u065F\u0670]")
        text = diacritics.sub("", text)

        text = text.replace("أ", "ا")
        text = text.replace("إ", "ا")
        text = text.replace("آ", "ا")
        text = text.replace("ٱ", "ا")

        text = text.replace("ى", "ي")
        text = text.replace("ئ", "ي")

        text = text.replace("ؤ", "و")

        text = text.replace("ـ", "")

        return text

    arabic_to_english_map = {
        "ا": "a",
        "ء": "2",
        "ب": "b",
        "ت": "t",
        "ة": "a",
        "ث": "th",
        "ج": "j",
        "ح": "7",
        "خ": "kh",
        "د": "d",
        "ذ": "dh",
        "ر": "r",
        "ز": "z",
        "س": "s",
        "ش": "sh",
        "ص": "s",
        "ض": "d",
        "ط": "t",
        "ظ": "z",
        "ع": "3",
        "غ": "gh",
        "ف": "f",
        "ق": "9",
        "ك": "k",
        "ل": "l",
        "م": "m",
        "ن": "n",
        "ه": "h",
        "و": "ou",
        "ي": "i",
        "لا": "la",
        " ": " ",
        "؟": "?",
        "،": ",",
        "؛": ";",
        "!": "!",
        ".": ".",
        ":": ":",
        "-": "-",
        "(": "(",
        ")": ")",
    }

    normalized_text = normalize_arabic(text)

    result = []
    i = 0

    while i < len(normalized_text):
        matched = False

        for length in range(3, 0, -1):
            if i + length <= len(normalized_text):
                substring = normalized_text[i : i + length]
                if substring in arabic_to_english_map:
                    result.append(arabic_to_english_map[substring])
                    i += length
                    matched = True
                    break

        if not matched:
            char = normalized_text[i]
            if char in arabic_to_english_map:
                result.append(arabic_to_english_map[char])
            else:
                result.append(char)
            i += 1

    return "".join(result)


def transliterate_darija(text: str, direction: Literal["to_latin", "to_arabic"]) -> str:
    if direction == "to_latin":
        if not contains_arabic(text):
            return text
        return transliterate_darija_arabic_to_latin(text)
    else:
        if contains_arabic(text):
            return text
        return transliterate_darija_latin_to_arabic(text)
