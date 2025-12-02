from config import settings
import os
import json
import pandas as pd
import spacy
from collections import Counter



def load_cefr_lexicon(language:str) -> dict:
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

    return lexicon


def build_texts_by_level_dataset(language: str) -> dict:
    if language == 'spanish':
        datasets = json.loads(settings.hf_repo_spanish_url)
    else:
        datasets = json.loads(settings.hf_repo_english_url)
    text_by_level = {
        'A1': [],
        'A2': [],
        'B1': [],
        'B2': [],
        'C1': [],
        'C2': []
    }
    print(datasets)
    for dataset in datasets:
        df = pd.read_json(datasets[dataset])
        for index, row in df.iterrows():
            level = row['cefr_level']
            text = row['text']
            if level in text_by_level:
                text_by_level[level].append(text)

    return text_by_level


# load_cefr_lexicon('english')


