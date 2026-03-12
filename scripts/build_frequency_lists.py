import spacy
from collections import Counter
import csv
import os

INPUT_FILE = "data/corpus/sample_wikipedia_text.txt"
OUTPUT_FILE = "data/output/lemma_pos_frequency.csv"

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

nlp = spacy.load("es_core_news_sm")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

doc = nlp(text)

# store (lemma, pos) tuples
tokens = [(token.lemma_.lower(), token.pos_) for token in doc if token.is_alpha]

freq = Counter(tokens)

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["rank", "lemma", "pos", "count"])

    for rank, ((lemma, pos), count) in enumerate(freq.most_common(), start=1):
        writer.writerow([rank, lemma, pos, count])

print("Lemma + POS frequency written to", OUTPUT_FILE)