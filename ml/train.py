import os
import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
)
import config


def load_and_split_dataset(data_file):
    dataset = load_dataset("json", data_files=data_file)
    dataset = dataset["train"].train_test_split(
        test_size=config.TRAIN_TEST_SPLIT, seed=config.RANDOM_SEED
    )
    print(f"Train samples: {len(dataset['train'])}")
    print(f"Test samples: {len(dataset['test'])}")
    return dataset


def load_model_and_tokenizer(model_name=None):
    if model_name is None:
        model_name = config.BASE_MODEL
        
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "mps" if torch.backends.mps.is_available() else "cpu"
    )
    model = model.to(device)
    print(f"Using device: {device}")
    print(f"Model loaded: {model_name}")
    
    return model, tokenizer


def create_preprocessing_function(tokenizer, src_lang, tgt_lang, src_field, tgt_field):
    def preprocess(examples):
        tokenizer.src_lang = src_lang
        tokenizer.tgt_lang = tgt_lang

        inputs = tokenizer(
            examples[src_field], 
            truncation=True, 
            max_length=config.MAX_INPUT_LENGTH
        )

        labels = tokenizer(
            text_target=examples[tgt_field], 
            truncation=True, 
            max_length=config.MAX_TARGET_LENGTH
        )

        inputs["labels"] = labels["input_ids"]
        return inputs

    return preprocess


def train_model(model, tokenizer, dataset, output_dir):
    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer, 
        model=model, 
        label_pad_token_id=-100, 
        pad_to_multiple_of=8
    )

    training_args = Seq2SeqTrainingArguments(
        output_dir=output_dir,
        eval_strategy="steps",
        save_strategy="steps",
        report_to="none",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        **config.TRAINING_CONFIG,
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        processing_class=tokenizer,
        data_collator=data_collator,
    )

    print(f"Starting training for {output_dir}...")
    trainer.train()

    final_dir = f"{output_dir}/final"
    trainer.save_model(final_dir)
    tokenizer.save_pretrained(final_dir)
    print(f"Training complete! Model saved to {final_dir}")


def test_translation(model, tokenizer, src_lang, tgt_lang, test_sentences, direction):
    print(f"\n{'=' * 70}")
    print(f"TESTING {direction}")
    print('=' * 70)
    
    for sentence in test_sentences:
        tokenizer.src_lang = src_lang
        inputs = tokenizer(sentence, return_tensors="pt").to(model.device)
        
        generated = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_lang),
            **config.INFERENCE_CONFIG,
        )
        
        translation = tokenizer.decode(generated[0], skip_special_tokens=True)
        
        src_label = "Darija" if direction == "DARIJA TO ENGLISH" else "English"
        tgt_label = "English" if direction == "DARIJA TO ENGLISH" else "Darija"
        
        print(f"\n{src_label}: {sentence}")
        print(f"{tgt_label}: {translation}")


def main():
    print("=" * 70)
    print("BIDIRECTIONAL TRAINING: DARIJA AND ENGLISH")
    print("=" * 70)

    if not os.path.exists(config.DATA_FILE):
        raise FileNotFoundError(f"Data file not found: {config.DATA_FILE}")

    dataset = load_and_split_dataset(config.DATA_FILE)

    # Darija to English
    print("\n" + "=" * 70)
    print("TRAINING MODEL 1: DARIJA TO ENGLISH")
    print("=" * 70)

    os.makedirs(config.OUTPUT_DIR_D2E, exist_ok=True)

    model_d2e, tokenizer_d2e = load_model_and_tokenizer()

    preprocess_d2e = create_preprocessing_function(
        tokenizer_d2e,
        src_lang=config.DARIJA_LANG_CODE,
        tgt_lang=config.ENGLISH_LANG_CODE,
        src_field="darija",
        tgt_field="english",
    )

    tokenized_d2e = dataset.map(
        preprocess_d2e,
        batched=True,
        remove_columns=dataset["train"].column_names,
        desc="Tokenizing Darija to English",
    )

    train_model(model_d2e, tokenizer_d2e, tokenized_d2e, config.OUTPUT_DIR_D2E)

    # Test Darija to English
    test_translation(
        model_d2e, 
        tokenizer_d2e,
        config.DARIJA_LANG_CODE,
        config.ENGLISH_LANG_CODE,
        config.TEST_DARIJA_SENTENCES,
        "DARIJA TO ENGLISH"
    )

    # Clean up first model from GPU
    del model_d2e
    torch.cuda.empty_cache() if torch.cuda.is_available() else None

    # English to Darija
    print("\n" + "=" * 70)
    print("TRAINING MODEL 2: ENGLISH TO DARIJA")
    print("=" * 70)

    os.makedirs(config.OUTPUT_DIR_E2D, exist_ok=True)

    model_e2d, tokenizer_e2d = load_model_and_tokenizer()

    preprocess_e2d = create_preprocessing_function(
        tokenizer_e2d,
        src_lang=config.ENGLISH_LANG_CODE,
        tgt_lang=config.DARIJA_LANG_CODE,
        src_field="english",
        tgt_field="darija",
    )

    tokenized_e2d = dataset.map(
        preprocess_e2d,
        batched=True,
        remove_columns=dataset["train"].column_names,
        desc="Tokenizing English to Darija",
    )

    train_model(model_e2d, tokenizer_e2d, tokenized_e2d, config.OUTPUT_DIR_E2D)

    # Test English to Darija
    test_translation(
        model_e2d,
        tokenizer_e2d,
        config.ENGLISH_LANG_CODE,
        config.DARIJA_LANG_CODE,
        config.TEST_ENGLISH_SENTENCES,
        "ENGLISH TO DARIJA"
    )

    print("\n" + "=" * 70)
    print("ALL TRAINING COMPLETE!")
    print(f"Model 1 (Darija to English): {config.OUTPUT_DIR_D2E}/final")
    print(f"Model 2 (English to Darija): {config.OUTPUT_DIR_E2D}/final")
    print("=" * 70)


if __name__ == "__main__":
    main()