import csv
from pathlib import Path

import spacy

# ── Paths ─────────────────────────────────────────────────────────────────────

SOURCES_TATOEBA   = Path("sources/tatoeba/tatoeba_es_en_20260307.tsv")
SOURCES_WIKIPEDIA = Path("sources/wikipedia/sample_wikipedia_text.txt")
SOURCES_LLM_DIR   = Path("sources/llm")

DATA_INTERIM_DIR   = Path("data/interim")
DATA_PROCESSED_DIR = Path("data/processed")

DATA_TATOEBA_CLEAN        = DATA_INTERIM_DIR  / "tatoeba_es_en_clean.csv"
DATA_TATOEBA_LEMMA_POS    = DATA_INTERIM_DIR  / "tatoeba_lemma_pos_freq.csv"
DATA_WIKIPEDIA_LEMMA_POS  = DATA_INTERIM_DIR  / "wikipedia_lemma_pos_freq.csv"
DATA_POS_LISTS_DIR        = DATA_INTERIM_DIR  / "tatoeba_pos_lists"
DATA_TOP_PHRASES          = DATA_PROCESSED_DIR / "wikipedia_top_phrases.csv"

MOCHI_DIR = Path("mochi")


# ── spaCy ─────────────────────────────────────────────────────────────────────

_nlp = None

def load_spacy():
    global _nlp
    if _nlp is None:
        print("   Loading spaCy model...")
        _nlp = spacy.load("es_core_news_sm")
    return _nlp


# ── Mochi helpers ─────────────────────────────────────────────────────────────

def parse_cards(input_path: Path):
    seen, cards = set(), []
    with open(input_path, encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) < 2:
                continue
            front, back = row[0].strip(), row[1].strip()
            if front and back:
                key = (front.lower(), back.lower())
                if key not in seen:
                    seen.add(key)
                    cards.append((front, back))
    return cards


def write_cards(cards, output_file: Path):
    with open(output_file, "w", encoding="utf-8") as f:
        for i, (front, back) in enumerate(cards):
            f.write(f"{front}\n---\n{back}\n")
            if i != len(cards) - 1:
                f.write("@@@\n")


def chunks(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]