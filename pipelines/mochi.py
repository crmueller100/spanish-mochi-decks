import csv
from pathlib import Path

from .utils import SOURCES_LLM_DIR, MOCHI_DIR, parse_cards, write_cards, chunks


def convert_to_mochi(deck_size: int = None):
    """Convert all CSVs in sources/llm/ to Mochi markdown cards → mochi/llm/"""
    print(">> Converting CSVs to Mochi cards...")

    for input_path in sorted(SOURCES_LLM_DIR.glob("*.csv")):
        cards = parse_cards(input_path)
        output_dir = MOCHI_DIR / input_path.parent.name
        output_dir.mkdir(parents=True, exist_ok=True)
        base_name = input_path.stem

        if deck_size is None:
            out = output_dir / f"{base_name}.md"
            write_cards(cards, out)
            print(f"   {len(cards):>4} cards → {out}")
        else:
            for i, chunk in enumerate(chunks(cards, deck_size), start=1):
                out = output_dir / f"{base_name}_{i:02}.md"
                write_cards(chunk, out)
                print(f"   {len(chunk):>4} cards → {out}")


def switch_columns(input_csv: Path, output_csv: Path):
    """Swap the first two columns of a CSV (e.g. ES→EN becomes EN→ES)."""
    print(f">> Switching columns: {input_csv.name} → {output_csv.name}")
    with open(input_csv, newline="", encoding="utf-8") as infile, \
         open(output_csv, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        for row in csv.reader(infile):
            if len(row) >= 2:
                writer.writerow([row[1], row[0]] + row[2:])
    print(f"   Wrote {output_csv}")