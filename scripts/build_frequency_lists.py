import spacy
from collections import Counter
import csv
import os
from tqdm import tqdm

INPUT_FILE = "corpus/sample_wikipedia_text.txt"
OUTPUT_FILE = "output/lemma_pos_frequency.csv"

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

print("Loading spaCy model...")
nlp = spacy.load("es_core_news_sm")

print("Reading corpus...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

print("Processing corpus...")
doc = nlp(text)

tokens = []

for token in tqdm(doc, desc="Processing tokens"):
    if token.is_alpha:
        tokens.append((token.lemma_.lower(), token.pos_))

freq = Counter(tokens)

print("Writing frequency list...")

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["rank", "lemma", "pos", "count"])

    for rank, ((lemma, pos), count) in enumerate(freq.most_common(), start=1):
        writer.writerow([rank, lemma, pos, count])

print("Lemma + POS frequency written to", OUTPUT_FILE)