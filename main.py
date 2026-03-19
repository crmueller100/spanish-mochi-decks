from pathlib import Path
from pipelines import (
    clean_tatoeba,
    build_tatoeba_frequency,
    split_pos_lists,
    build_frequency_lists,
    extract_phrases,
    convert_to_mochi,
    tatoeba_to_mochi,
    switch_columns,
    SOURCES_LLM_DIR
)

# "llm" or "tatoeba" or "tatoeba_to_csv"
PIPELINE = "tatoeba"

if PIPELINE == "tatoeba":
    clean_tatoeba()
    build_tatoeba_frequency()  # This job takes a long time
    split_pos_lists()
    build_frequency_lists()
    extract_phrases()

elif PIPELINE == "llm":
    convert_to_mochi()
    # convert_to_mochi(deck_size=100)

    # switch_columns(
    #     SOURCES_LLM_DIR / "phrases_es_to_en.csv",
    #     SOURCES_LLM_DIR / "phrases_en_to_es.csv",
    # )
elif PIPELINE == "tatoeba_to_csv":
    tatoeba_to_mochi(
        Path("data/tatoeba_es_en_clean.csv"),
        total_cards=200,
        deck_size=100,
        randomize=True,
    )