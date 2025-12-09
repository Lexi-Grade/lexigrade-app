from config import settings
import os
import json
from datasets import load_dataset
import spacy
from collections import Counter



def load_cefr_lexicon(language:str):
    if language == 'english':
        nlp_model = "en_core_web_sm"
    else:
        nlp_model = "es_core_news_sm"
    texts_by_level = build_texts_by_level_dataset(language)
    nlp = spacy.load(nlp_model)
    lexicon = {}
    frequencies = {}

    for level, texts in texts_by_level.items():
        counter = Counter()

        for doc in nlp.pipe(texts, batch_size=1000):
            tokens = [w.lemma_.lower() for w in doc
                      if w.is_alpha]
            counter.update(tokens)

        for w, freq in counter.items():
            if w not in lexicon:
                lexicon[w] = level
            else:
                lexicon[w] = min(lexicon[w], level)
            if w not in frequencies:
                frequencies[w] = freq
            else:
                frequencies[w] += freq
    total_tokens = sum(frequencies.values())
    with open(os.path.join(settings.datasets_base_path, language, "cefr_lexicon.json"), "w", encoding="utf-8") as f:
        json.dump(lexicon, f, ensure_ascii=False, indent=4)
    with open(os.path.join(settings.datasets_base_path, language, f"cefr_frequencies.json"), "w", encoding="utf-8") as f:
        json.dump({"total_tokens": total_tokens, "freqs": frequencies}, f, ensure_ascii=False, indent=2)


def build_texts_by_level_dataset(language: str) -> dict:
    if language == 'english':
        universal_cefr_datasets = settings.universal_cefr_english_datasets
    else:
        universal_cefr_datasets = settings.universal_cefr_spanish_datasets
    text_by_level = {
        'A1': [],
        'A2': [],
        'B1': [],
        'B2': [],
        'C1': [],
        'C2': []
    }
    for universal_cefr_dataset in universal_cefr_datasets.split(','):
        dataset = load_dataset(
            universal_cefr_dataset,
            split="train",
        )
        for item in dataset:
            cefr_level = item["cefr_level"]
            if cefr_level != 'NA':
                cefr_level = cefr_level.replace('+','')
                text_by_level[cefr_level].append(item["text"])

    return text_by_level

load_cefr_lexicon('spanish')