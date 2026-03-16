import csv
from collections import Counter, defaultdict

from tqdm import tqdm

from .utils import (
    SOURCES_TATOEBA, DATA_TATOEBA_CLEAN, DATA_TATOEBA_FREQ_POS,
    DATA_POS_LISTS_DIR, load_spacy,
)


def clean_tatoeba():
    """Deduplicate and clean raw Tatoeba TSV → data/tatoeba_es_en_clean.csv"""
    print(">> Cleaning Tatoeba pairs...")
    seen = set()
    DATA_TATOEBA_CLEAN.parent.mkdir(parents=True, exist_ok=True)

    with open(SOURCES_TATOEBA, encoding="utf-8") as infile, \
         open(DATA_TATOEBA_CLEAN, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.reader(infile, delimiter="\t")
        writer = csv.writer(outfile)
        writer.writerow(["spanish", "english"])

        for row in reader:
            if len(row) < 4:
                continue
            es, en = row[1].strip(), row[3].strip()
            if es and en and es not in seen:
                writer.writerow([es, en])
                seen.add(es)

    print(f"   Wrote {DATA_TATOEBA_CLEAN}")


def build_tatoeba_frequency():
    """Lemma + POS frequency from Tatoeba sentences → data/tatoeba_frequency_pos.csv"""
    print(">> Building Tatoeba frequency list...")
    nlp = load_spacy()

    sentences = []
    with open(DATA_TATOEBA_CLEAN, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sentences.append(row["spanish"])

    counter = Counter()
    for doc in tqdm(nlp.pipe(sentences, batch_size=1000), total=len(sentences)):
        for token in doc:
            if token.is_alpha:
                counter[(token.lemma_.lower(), token.pos_)] += 1

    DATA_TATOEBA_FREQ_POS.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_TATOEBA_FREQ_POS, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "lemma", "pos", "count"])
        for rank, ((lemma, pos), count) in enumerate(counter.most_common(), start=1):
            writer.writerow([rank, lemma, pos, count])

    print(f"   Wrote {DATA_TATOEBA_FREQ_POS}")


def split_pos_lists():
    """Split tatoeba_frequency_pos.csv into per-POS CSVs → data/tatoeba_pos_lists/"""
    print(">> Splitting POS lists...")
    LIMITS = {"VERB": 1000, "NOUN": 1000, "ADJ": 500, "ADV": 500}
    DATA_POS_LISTS_DIR.mkdir(parents=True, exist_ok=True)

    pos_data = defaultdict(list)
    with open(DATA_TATOEBA_FREQ_POS, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["pos"] in LIMITS:
                pos_data[row["pos"]].append(row)

    for pos, rows in pos_data.items():
        limit = LIMITS[pos]
        out = DATA_POS_LISTS_DIR / f"top_{limit}_{pos.lower()}.csv"
        with open(out, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["rank", "lemma", "count"])
            for i, row in enumerate(rows[:limit], start=1):
                writer.writerow([i, row["lemma"], row["count"]])
        print(f"   Wrote {out}")