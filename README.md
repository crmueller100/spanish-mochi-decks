# mochi-spanish-flashcards
Spanish vocabulary datasets and Mochi flashcard decks (verbs, nouns, conjugations, and grammar).

# How to use
### To converts CSVs into Mochi markdown files
If you make a change to a file within to a data files, you can regenerate the Mochi markdown by running this:
```bash
python3 scripts/convert_csv_to_mochi_cards.py filename.csv [--deck-size 50]
```
Note that if you wanted to break up the larger CSVs into decks of more manageable size, there is an optional argument to do that.

To rerun all files within the `claude_generated_data/` directory, you can do:
```bash
for csv in claude_generated_data/*/*.csv; do
    python3 scripts/convert_csv_to_mochi_cards.py "$csv"
done
```

_Conjugations are currently not generated with this script._

### To import into mochi
Files within the `mochi/` folder can be imported into the [Mochi](https://mochi.cards/) app. Simply select "Markdown" and choose `@@@` for the delimiter. This will import each item as its own card
