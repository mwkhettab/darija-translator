import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from core.config import settings


DEVICE = (
    "cuda"
    if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available() else "cpu"
)

DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32


d2e_tokenizer = None
d2e_model = None

e2d_tokenizer = None
e2d_model = None


def init_models() -> None:
    global d2e_tokenizer, d2e_model, e2d_tokenizer, e2d_model

    if d2e_model is not None:

        return

    d2e_tokenizer = AutoTokenizer.from_pretrained(settings.d2e_model_id)
    d2e_tokenizer.src_lang = "ary_Arab"

    d2e_model = (
        AutoModelForSeq2SeqLM.from_pretrained(
            settings.d2e_model_id,
            torch_dtype=DTYPE if DEVICE == "cuda" else None,
        )
        .to(DEVICE)
        .eval()
    )

    e2d_tokenizer = AutoTokenizer.from_pretrained(settings.e2d_model_id)
    e2d_tokenizer.src_lang = "eng_Latn"

    e2d_model = (
        AutoModelForSeq2SeqLM.from_pretrained(
            settings.e2d_model_id,
            torch_dtype=DTYPE if DEVICE == "cuda" else None,
        )
        .to(DEVICE)
        .eval()
    )


def translate_darija_to_english(text: str) -> str:
    if d2e_model is None:
        raise RuntimeError("Models not initialized.")

    inputs = d2e_tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
    ).to(DEVICE)

    with torch.no_grad():
        output = d2e_model.generate(
            **inputs,
            forced_bos_token_id=d2e_tokenizer.convert_tokens_to_ids("eng_Latn"),
            max_new_tokens=512,
            num_beams=5,
            do_sample=False,
        )

    return d2e_tokenizer.decode(
        output[0],
        skip_special_tokens=True,
    ).strip()


def translate_english_to_darija(text: str) -> str:
    if e2d_model is None:
        raise RuntimeError("Models not initialized.")

    inputs = e2d_tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
    ).to(DEVICE)

    with torch.no_grad():
        output = e2d_model.generate(
            **inputs,
            forced_bos_token_id=e2d_tokenizer.convert_tokens_to_ids("ary_Arab"),
            max_new_tokens=512,
            num_beams=5,
            do_sample=False,
        )

    return e2d_tokenizer.decode(
        output[0],
        skip_special_tokens=True,
    ).strip()
