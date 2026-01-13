import argparse
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import config


class TranslationModel:

    def __init__(self, model_id, src_lang, tgt_lang):
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

        self.device = torch.device(
            "cuda"
            if torch.cuda.is_available()
            else "mps" if torch.backends.mps.is_available() else "cpu"
        )
        self.model = self.model.to(self.device)

        self.src_lang = src_lang
        self.tgt_lang = tgt_lang

        print(f"Model loaded from {model_id}")
        print(f"Using device: {self.device}")
        print(f"Translation: {src_lang} → {tgt_lang}")

    def translate(self, text, max_length=None, num_beams=None, early_stopping=None):
        if max_length is None:
            max_length = config.INFERENCE_CONFIG["max_length"]
        if num_beams is None:
            num_beams = config.INFERENCE_CONFIG["num_beams"]
        if early_stopping is None:
            early_stopping = config.INFERENCE_CONFIG["early_stopping"]

        self.tokenizer.src_lang = self.src_lang

        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)

        generated = self.model.generate(
            **inputs,
            forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(self.tgt_lang),
            max_length=max_length,
            num_beams=num_beams,
            early_stopping=early_stopping,
        )

        return self.tokenizer.decode(generated[0], skip_special_tokens=True)

    def translate_batch(
        self, texts, max_length=None, num_beams=None, early_stopping=None
    ):

        return [
            self.translate(text, max_length, num_beams, early_stopping)
            for text in texts
        ]


def load_darija_to_english_model(model_id=None):
    if model_id is None:
        model_id = config.HF_MODEL_D2E

    return TranslationModel(
        model_id, src_lang=config.DARIJA_LANG_CODE, tgt_lang=config.ENGLISH_LANG_CODE
    )


def load_english_to_darija_model(model_id=None):
    if model_id is None:
        model_id = config.HF_MODEL_E2D

    return TranslationModel(
        model_id, src_lang=config.ENGLISH_LANG_CODE, tgt_lang=config.DARIJA_LANG_CODE
    )


def interactive_mode(direction):
    print(f"\n{'=' * 70}")
    print(f"INTERACTIVE TRANSLATION MODE: {direction}")
    print("=" * 70)
    print("Type 'quit' or 'exit' to stop")
    print("=" * 70 + "\n")

    if direction == "d2e":
        model = load_darija_to_english_model()
        src_label, tgt_label = "Darija", "English"
    else:
        model = load_english_to_darija_model()
        src_label, tgt_label = "English", "Darija"

    while True:
        try:
            text = input(f"\n{src_label}: ").strip()

            if text.lower() in ["quit", "exit", "q"]:
                print("\nGoodbye!")
                break

            if not text:
                continue

            translation = model.translate(text)
            print(f"{tgt_label}: {translation}")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Translate between Darija and English")

    parser.add_argument(
        "direction",
        choices=["d2e", "e2d"],
        help="Translation direction: 'd2e' (Darija→English) or 'e2d' (English→Darija)",
    )

    parser.add_argument(
        "--text",
        type=str,
        help="Text to translate (if not provided, enters interactive mode)",
    )

    parser.add_argument(
        "--model-id",
        type=str,
        help="Model identifier or path to model directory (optional, uses default if not specified)",
    )

    parser.add_argument(
        "--batch",
        action="store_true",
        help="Translate multiple sentences (one per line from stdin)",
    )

    args = parser.parse_args()

    if args.direction == "d2e":
        model = load_darija_to_english_model(args.model_id)
        src_label, tgt_label = "Darija", "English"
    else:
        model = load_english_to_darija_model(args.model_id)
        src_label, tgt_label = "English", "Darija"

    if args.text:
        translation = model.translate(args.text)
        print(f"{src_label}: {args.text}")
        print(f"{tgt_label}: {translation}")

    elif args.batch:
        print(f"Enter sentences to translate (one per line, Ctrl+D when done):")
        import sys

        texts = [line.strip() for line in sys.stdin if line.strip()]
        translations = model.translate_batch(texts)

        print(f"\n{'=' * 70}")
        print("TRANSLATIONS")
        print("=" * 70)
        for text, translation in zip(texts, translations):
            print(f"\n{src_label}: {text}")
            print(f"{tgt_label}: {translation}")

    else:
        interactive_mode(args.direction)


if __name__ == "__main__":
    main()
