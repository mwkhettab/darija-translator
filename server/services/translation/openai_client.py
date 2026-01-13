from openai import OpenAI
from core.config import settings
from utils.languages import get_language_name

client = OpenAI(api_key=settings.openai_api_key)


def transliterate_darija_latin_to_arabic(text: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        temperature=0,
        instructions=(
            "You are a Moroccan Darija linguist.\n"
            "Transliterate Darija from Latin script to Arabic script.\n\n"
            "RULES:\n"
            "- Transliteration ONLY (not translation)\n"
            "- Moroccan Darija spelling, not MSA\n"
            "- Numerals: 7→ح, 3→ع, 9→ق, 2→ء\n"
            "- No diacritics or tashkeel\n"
            "- Output ONLY the converted text"
        ),
        input=text,
    )

    return response.output_text.strip()


def translate(
    source_language: str,
    target_language: str,
    source_text: str,
    english_reference: str = "",
) -> str:
    print(source_language, target_language, source_text, english_reference)
    source_language_name = get_language_name(lang_code=source_language)
    target_language_name = get_language_name(lang_code=target_language)
    prompt = f"""
You are a professional human translator.

Your task is to TRANSLATE the source text from {source_language_name}
into {target_language_name}. This is a translation task, not a summary,
rewrite, explanation, or commentary.

AUTHORITATIVE SOURCE:
- The SOURCE text is the sole authority for meaning.
- The English reference is provided ONLY to clarify ambiguity.
- The English reference MUST NOT override, replace, or reinterpret
  the source text under any circumstances.

STRICT OUTPUT RULES (ABSOLUTE PRIORITY):
- ALWAYS produce a translation into {target_language_name}
- Output MUST be written ONLY in {target_language_name}
- Output MUST NOT contain {source_language_name}
- DO NOT include explanations, notes, comments, or formatting
- DO NOT add, omit, or infer information
- Preserve the original tone, register, intent, and meaning
- Avoid literal calques if they sound unnatural in the target language
- If the target language is Darija, use natural spoken Darija
- No diacritics or tashkeel in Arabic script
- Any violation of these rules makes the output invalid

SOURCE TEXT ({source_language_name}):
\"\"\"{source_text}\"\"\"

{english_reference and f'''
ENGLISH REFERENCE (NON-AUTHORITATIVE, FOR DISAMBIGUATION ONLY):
\"\"\"{english_reference}\"\"\"
'''
}
"""

    response = client.responses.create(
        model="gpt-4.1",
        temperature=0.2,
        max_output_tokens=400,
        input=prompt,
    )
    print(response.output_text)
    print(response)
    return response.output_text.strip()
