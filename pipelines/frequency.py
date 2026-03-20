import csv
from collections import Counter

from tqdm import tqdm

from .utils import (
    SOURCES_WIKIPEDIA, DATA_WIKIPEDIA_LEMMA_POS, DATA_TOP_PHRASES, load_spacy,
)


def build_frequency_lists():
    """Lemma + POS frequency from Wikipedia corpus → data/lemma_pos_frequency.csv"""
    print(">> Building Wikipedia frequency list...")
    nlp = load_spacy()

    text = SOURCES_WIKIPEDIA.read_text(encoding="utf-8")
    doc = nlp(text)

    freq = Counter(
        (token.lemma_.lower(), token.pos_)
        for token in tqdm(doc, desc="Processing tokens")
        if token.is_alpha
    )

    DATA_WIKIPEDIA_LEMMA_POS.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_WIKIPEDIA_LEMMA_POS, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "lemma", "pos", "count"])
        for rank, ((lemma, pos), count) in enumerate(freq.most_common(), start=1):
            writer.writerow([rank, lemma, pos, count])

    print(f"   Wrote {DATA_WIKIPEDIA_LEMMA_POS}")


def extract_phrases():
    """Extract top bigrams/trigrams from Wikipedia corpus → data/processed/wikipedia_top_phrases.csv"""
    print(">> Extracting phrases...")
    TOP_BIGRAMS, TOP_TRIGRAMS, MIN_COUNT = 1500, 500, 3
    nlp = load_spacy()

    text = SOURCES_WIKIPEDIA.read_text(encoding="utf-8")
    doc = nlp(text)

    tokens = []
    for token in tqdm(doc, desc="Collecting tokens"):
        if token.is_alpha:
            tokens.append(token.text.lower())

    bigrams = Counter()
    for i in range(len(tokens) - 1):
        w1, w2 = tokens[i], tokens[i + 1]
        if not (nlp.vocab[w1].is_stop and nlp.vocab[w2].is_stop):
            bigrams[f"{w1} {w2}"] += 1

    trigrams = Counter()
    for i in range(len(tokens) - 2):
        w1, w2, w3 = tokens[i], tokens[i + 1], tokens[i + 2]
        if sum(nlp.vocab[w].is_stop for w in (w1, w2, w3)) < 2:
            trigrams[f"{w1} {w2} {w3}"] += 1

    bigrams  = {p: c for p, c in bigrams.items()  if c >= MIN_COUNT}
    trigrams = {p: c for p, c in trigrams.items() if c >= MIN_COUNT}

    DATA_TOP_PHRASES.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_TOP_PHRASES, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "phrase", "count", "n"])
        rank = 1
        for phrase, count in Counter(bigrams).most_common(TOP_BIGRAMS):
            writer.writerow([rank, phrase, count, 2]); rank += 1
        for phrase, count in Counter(trigrams).most_common(TOP_TRIGRAMS):
            writer.writerow([rank, phrase, count, 3]); rank += 1

    print(f"   Wrote {DATA_TOP_PHRASES}")