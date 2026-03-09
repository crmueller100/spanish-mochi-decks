#!/usr/bin/env python3

import sys
import argparse
from pathlib import Path
import csv


def parse_csv(input_path):
    seen = set()
    cards = []

    with open(input_path, "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for line_number, row in enumerate(reader, start=2):  # header is line 1
            front = row.get("phrase", "").strip()
            back = row.get("translation", "").strip()

            if not front or not back:
                print(f"Skipping line {line_number}: missing phrase or translation")
                continue

            key = (front.lower(), back.lower())
            if key in seen:
                continue

            seen.add(key)
            cards.append((front, back))

    return cards


def write_cards(cards, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for i, (front, back) in enumerate(cards):
            f.write(f"{front}\n")
            f.write("---\n")
            f.write(f"{back}\n")
            if i != len(cards) - 1:
                f.write("@@@\n")


def chunk_cards(cards, size):
    for i in range(0, len(cards), size):
        yield cards[i:i + size]


def main():
    parser = argparse.ArgumentParser(description="Convert CSV vocab into Mochi markdown cards.")
    parser.add_argument("input_csv", help="Input CSV file")
    parser.add_argument("--deck-size", type=int, default=None, help="Split output into decks of N cards")

    args = parser.parse_args()

    input_path = Path(args.input_csv).resolve()

    if not input_path.exists():
        print("Input file does not exist")
        sys.exit(1)

    repo_root = Path(__file__).resolve().parent.parent

    category = input_path.parent.name
    output_dir = repo_root / "mochi" / category
    output_dir.mkdir(parents=True, exist_ok=True)

    base_name = input_path.stem

    cards = parse_csv(input_path)

    if args.deck_size is None:
        output_file = output_dir / f"{base_name}.md"
        write_cards(cards, output_file)
        print(f"Wrote {len(cards)} cards → {output_file}")
    else:
        chunks = list(chunk_cards(cards, args.deck_size))
        for i, chunk in enumerate(chunks, start=1):
            output_file = output_dir / f"{base_name}_{i:02}.md"
            write_cards(chunk, output_file)
            print(f"Wrote {len(chunk)} cards → {output_file}")


if __name__ == "__main__":
    main()