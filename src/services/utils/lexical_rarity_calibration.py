from config import settings
import os
import json
from services.datasets import build_texts_by_level_dataset
import math
import statistics
from pathlib import Path
import spacy

ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"]
DATASET_ENGLISH_BASEPATH = os.path.join(settings.datasets_base_path, "english")
DATASET_SPANISH_BASEPATH = os.path.join(settings.datasets_base_path, "spanish")

def main(languages: list[str]):
    for language in languages:
        if language == "english":
            spacy_model = "en_core_web_sm"
            language_base_dataset_path = DATASET_ENGLISH_BASEPATH
        else:
            spacy_model = "es_core_news_sm"
            language_base_dataset_path = DATASET_ENGLISH_BASEPATH

        print(f"🔄 Loading {language} spaCy model...")
        nlp = spacy.load(spacy_model)

        print(f"🔄 Loading {language} CEFR dataset by level...")
        texts_by_level = build_texts_by_level_dataset(language)

        print(f"🔄 Loading {language} frequencies...")
        freq_file = Path(os.path.join(language_base_dataset_path, "cefr_frequencies.json"))
        data = json.loads(freq_file.read_text(encoding="utf-8"))

        if "freqs" in data:
            freqs = data["freqs"]
            total_tokens = data["total_tokens"]
        else:
            freqs = data
            total_tokens = sum(freqs.values())

        print(f"🧮 Frequencies loaded ({len(freqs):,} lemmas, {total_tokens:,} tokens).") #

        print("\n📏 Starting calibration...\n")
        thresholds, stats = calibrate_thresholds(texts_by_level, nlp, freqs, total_tokens)

        out_file = Path(os.path.join(language_base_dataset_path, "cefr_rarity_thresholds.json"))
        out_file.write_text(
            json.dumps({
                "thresholds": thresholds,
                "statistics": stats
            }, indent=2, ensure_ascii=False),
            encoding="utf-8",
            errors="replace"
        )

        print("\n✅ Thresholds Calibrated successfully!")
        print(f"📁 Saved at: {out_file.absolute()}")

        print("\n📊 Final Thresholds:")
        print(json.dumps(thresholds, indent=2))



def normalize_level(level_raw: str):
    if not isinstance(level_raw, str):
        return None

    level = level_raw.strip().upper()
    if level in ORDER:
        return level

    return None



def compute_rarity(freq, total_tokens, V):
    prob = (freq + 1) / (total_tokens + V)
    return -math.log(prob)


def rarity_for_text(text, nlp, freqs, total_tokens):
    doc = nlp(text)
    V = len(freqs)
    rarities = []

    for token in doc:
        if not token.is_alpha:
            continue
        if token.pos_ == "PROPN" or token.ent_type_ in ["PERSON", "GPE", "ORG"]:
            continue

        lemma = token.lemma_.lower()
        freq = freqs.get(lemma, 0)

        rarity = compute_rarity(freq, total_tokens, V)
        rarities.append(rarity)

    if not rarities:
        return None

    return sum(rarities) / len(rarities)


def calibrate_thresholds(texts_by_level, nlp, freqs, total_tokens):
    thresholds = {}
    stats = {}

    for level_raw, texts in texts_by_level.items():
        level = normalize_level(level_raw)
        if level is None:
            print(f"[IGNORED] Invalid level found: {level_raw}")
            continue

        print(f"Calibrating CEFR level {level}... ({len(texts)} texts)")

        rarity_scores = []

        for txt in texts:
            score = rarity_for_text(txt, nlp, freqs, total_tokens)
            if score is not None:
                rarity_scores.append(score)

        if len(rarity_scores) < 10:
            print(f"[WARNING] Level {level} has few texts ({len(rarity_scores)}). Threshold will be less accurate.")

        rarity_scores.sort()

        if rarity_scores:
            p90 = rarity_scores[int(len(rarity_scores) * 0.90)]
            mean = statistics.mean(rarity_scores)
            std = statistics.pstdev(rarity_scores) if len(rarity_scores) > 1 else 0

            thresholds[level] = p90
            stats[level] = {
                "samples": len(rarity_scores),
                "mean": mean,
                "std": std,
                "p90": p90
            }
        else:
            thresholds[level] = None
            stats[level] = {"samples": 0}

    return thresholds, stats



if __name__ == "__main__":
    main(["english"])

