# Darija Translator 🇲🇦

A free, open-source Darija (Moroccan Arabic) translation app supporting 20+ languages. The system combines a fine-tuned Darija model with high-quality multilingual models to deliver accurate translations for real, informal Darija.

Try it [here.](https://darija-translator.vercel.app)

---

## Features

- 🌍 **Multiple Languages** – Translate to/from Darija and major world languages  
**🔁 Model-Aware Pipeline** – Uses a Darija-specific model for Moroccan Arabic and multilingual models for other languages
- 🧠 **Custom Darija Model** – Fine-tuned specifically on real Darija data  
- 🖥 **Multilingual UI** – English, French, Arabic  
- 💸 **Free & Open Source**

---

## Architecture

`client/` - SvelteKit frontend

`server/` - FastAPI backend

`model/` - Training & inference scripts


---

## Custom Model

- **Base**:  
  [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M)

- **Training Data**:
  - [Darija Open Dataset](https://github.com/darija-open-dataset/dataset)
  - Curated real-world Darija sentence pairs

- **Goal**: Accurate informal Darija, including code-switching

👉 Models on Hugging Face:  
https://huggingface.co/collections/mwkhettab/darija-english-translation-nllb-200-distilled

---

## Examples

### Darija → English

**Input**

Kidayr ta9s barra daba?

**Output**

How’s the weather outside right now?


---

### English → Darija

**Input**

Where can I find a restaurant? I'm really hungry.

**Output**

فين نقدر نلقى ريسطورة؟ أنا جوع بزاف

**Latin**

fin n9dr nl9a ristoura? ana jou3an bzaf

If you want a lightweight preprocessing layer before translation, [darija-tools](https://github.com/Samielakkad/darija-tools) covers Moroccan Darija normalization and rule-based Arabizi → Arabic transliteration.

---

## Tech Stack

- Frontend: SvelteKit + Paraglide
- Backend: FastAPI
- ML: PyTorch, Hugging Face
- Models: NLLB + OpenAI

---

If you find this useful, please leave a ⭐
