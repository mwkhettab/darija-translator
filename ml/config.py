import os

# Data Configuration
DATA_FILE = "./data/sentences.jsonl"
TRAIN_TEST_SPLIT = 0.1
RANDOM_SEED = 42

# Model Configuration
BASE_MODEL = "facebook/nllb-200-distilled-600M"
HF_MODEL_D2E = "mwkhettab/nllb-200-darija-en"
HF_MODEL_E2D = "mwkhettab/nllb-200-en-darija"

# Language codes for NLLB-200
DARIJA_LANG_CODE = "ary_Arab"
ENGLISH_LANG_CODE = "eng_Latn"

# Output directories for trained models
OUTPUT_DIR_D2E = "./nllb-200-darija-en"  # Darija to English model
OUTPUT_DIR_E2D = "./nllb-200-en-darija"  # English to Darija model

# Training hyperparameters
TRAINING_CONFIG = {
    "per_device_train_batch_size": 4,
    "per_device_eval_batch_size": 4,
    "gradient_accumulation_steps": 4,
    "learning_rate": 2e-5,
    "num_train_epochs": 3,
    "warmup_steps": 200,
    "weight_decay": 0.0,
    "fp16": True,
    "save_steps": 1000,
    "eval_steps": 1000,
    "logging_steps": 200,
    "save_total_limit": 3,
    "max_grad_norm": 1.0,
}

# Maximum sequence lengths
MAX_INPUT_LENGTH = 128
MAX_TARGET_LENGTH = 128

# Inference configuration
INFERENCE_CONFIG = {
    "max_length": 128,
    "num_beams": 5,
    "early_stopping": True,
}

# Test sentences for quick evaluation
TEST_DARIJA_SENTENCES = [
    "كيف داير؟",
    "راه خاصنا نمشيو دابا",
    "هاد الخدمة صعيبة بزاف",
    "هوما مخبّين شي حاجة, أنا متيقّن!",
    "غانمشي!",
]

TEST_ENGLISH_SENTENCES = [
    "How are you?",
    "We need to go now",
    "This work is very difficult",
    "They are hiding something, I'm sure!",
    "I will go!",
]
