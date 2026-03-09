import csv
from pathlib import Path

INPUT_FILE = Path("data/phrases/phrases_es_to_en.csv")
OUTPUT_FILE = Path("data/phrases/phrases_en_to_es.csv")

with open(INPUT_FILE, newline='', encoding="utf-8") as infile, \
     open(OUTPUT_FILE, 'w', newline='', encoding="utf-8") as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        if len(row) < 2:
            # Skip invalid rows
            continue
        # Swap the first two columns, keep the rest
        swapped_row = [row[1], row[0]] + row[2:]
        writer.writerow(swapped_row)

print(f"Swapped columns written to {OUTPUT_FILE}")
