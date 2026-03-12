import csv

INPUT_FILE = "corpus/tatoeba_es_en.tsv"
OUTPUT_FILE = "data/tatoeba_es_en_clean.csv"

seen = set()

with open(INPUT_FILE, encoding="utf-8") as infile, open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:
    reader = csv.reader(infile, delimiter="\t")
    writer = csv.writer(outfile)

    writer.writerow(["spanish", "english"])

    for row in reader:
        # skip malformed rows
        if len(row) < 4:
            continue

        es = row[1].strip()
        en = row[3].strip()

        if not es or not en:
            continue

        if es not in seen:
            writer.writerow([es, en])
            seen.add(es)

print("Unique sentence pairs written.")