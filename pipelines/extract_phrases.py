import spacy
from collections import Counter
import csv
import os
from tqdm import tqdm

INPUT_FILE = "corpus/sample_wikipedia_text.txt"
OUTPUT_FILE = "data/top_phrases.csv"

TOP_BIGRAMS = 1500
TOP_TRIGRAMS = 500
MIN_COUNT = 3

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

print("Loading spaCy model...")
nlp = spacy.load("es_core_news_sm")

print("Reading corpus...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

print("Processing corpus...")
doc = nlp(text)

tokens = []
pos_tags = []

for token in tqdm(doc, desc="Collecting tokens"):
    if token.is_alpha:
        tokens.append(token.text.lower())
        pos_tags.append(token.pos_)

bigrams = Counter()
trigrams = Counter()

print("Building bigrams...")
for i in tqdm(range(len(tokens) - 1)):
    w1, w2 = tokens[i], tokens[i+1]
    p1, p2 = pos_tags[i], pos_tags[i+1]

    # skip stopword-only phrases like "de la"
    if nlp.vocab[w1].is_stop and nlp.vocab[w2].is_stop:
        continue

    phrase = f"{w1} {w2}"
    bigrams[phrase] += 1

print("Building trigrams...")
for i in tqdm(range(len(tokens) - 2)):
    w1, w2, w3 = tokens[i], tokens[i+1], tokens[i+2]
    p1, p2, p3 = pos_tags[i], pos_tags[i+1], pos_tags[i+2]

    # skip phrases composed mostly of stopwords
    stop_count = sum([
        nlp.vocab[w1].is_stop,
        nlp.vocab[w2].is_stop,
        nlp.vocab[w3].is_stop
    ])

    if stop_count >= 2:
        continue

    phrase = f"{w1} {w2} {w3}"
    trigrams[phrase] += 1

print("Filtering by minimum frequency...")

bigrams = {p: c for p, c in bigrams.items() if c >= MIN_COUNT}
trigrams = {p: c for p, c in trigrams.items() if c >= MIN_COUNT}

print("Writing results...")

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["rank", "phrase", "count", "n"])

    rank = 1

    for phrase, count in Counter(bigrams).most_common(TOP_BIGRAMS):
        writer.writerow([rank, phrase, count, 2])
        rank += 1

    for phrase, count in Counter(trigrams).most_common(TOP_TRIGRAMS):
        writer.writerow([rank, phrase, count, 3])
        rank += 1

print("Top phrases written to", OUTPUT_FILE)