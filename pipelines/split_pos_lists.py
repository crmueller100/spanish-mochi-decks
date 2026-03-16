import csv
import os
from collections import defaultdict

INPUT_FILE = "data/tatoeba_frequency_pos.csv"
OUTPUT_DIR = "data/tatoeba_pos_lists"

os.makedirs(OUTPUT_DIR, exist_ok=True)

LIMITS = {
    "VERB": 1000,
    "NOUN": 1000,
    "ADJ": 500,
    "ADV": 500,
}

pos_data = defaultdict(list)

print("Reading frequency list...")

with open(INPUT_FILE, encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        pos = row["pos"]

        if pos in LIMITS:
            pos_data[pos].append(row)

print("Writing POS lists...")

for pos, rows in pos_data.items():
    limit = LIMITS[pos]

    output_file = f"{OUTPUT_DIR}/top_{limit}_{pos.lower()}.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "lemma", "count"])

        for i, row in enumerate(rows[:limit], start=1):
            writer.writerow([i, row["lemma"], row["count"]])

    print("Wrote", output_file)

print("Done.")