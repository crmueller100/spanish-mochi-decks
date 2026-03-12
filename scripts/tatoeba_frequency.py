import csv
from collections import Counter
import spacy
from tqdm import tqdm
import os

INPUT_FILE = "data/tatoeba_es_en_clean.csv"
OUTPUT_FILE = "data/tatoeba_frequency_pos.csv"

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

print("Loading spaCy model...")
nlp = spacy.load("es_core_news_sm")

counter = Counter()

print("Reading sentences...")

sentences = []

with open(INPUT_FILE, encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        sentences.append(row["spanish"])

print("Processing sentences with spaCy...")

for doc in tqdm(nlp.pipe(sentences, batch_size=1000)):
    for token in doc:
        if token.is_alpha:
            lemma = token.lemma_.lower()
            pos = token.pos_

            counter[(lemma, pos)] += 1

print("Writing results...")

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["rank", "lemma", "pos", "count"])

    for rank, ((lemma, pos), count) in enumerate(counter.most_common(), start=1):
        writer.writerow([rank, lemma, pos, count])

print("Done.")