# Darija Translation Dataset

Training data for fine-tuning the Darija translation models must go in this directory

## File Structure

All training data must be stored in `sentences.jsonl` (JSON Lines format).

## Format Requirements

Each line must contain a single JSON object with English-Darija sentence pairs:

```json
{"english": "How are you today?", "darija": "كيداير اليوم؟"}
{"english": "I'm learning Darija.", "darija": "أنا كنتعلم الدارجة."}
...
```

### Important Notes

Use Arabic script for Darija
```json
{"english": "Hello", "darija": "السلام"}
```

Do NOT use Latinized Arabic 
```json
{"english": "Hello", "darija": "salam"} // this is wrong
```

## Data Source

The primary dataset is from [Darija Open Dataset](https://github.com/darija-open-dataset/dataset),  with additional curated sentence pairs.