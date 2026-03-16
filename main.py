from pipelines import (
    clean_tatoeba,
    build_tatoeba_frequency,
    split_pos_lists,
    build_frequency_lists,
    extract_phrases,
    convert_to_mochi,
    switch_columns,
    SOURCES_LLM_DIR,
)

clean_tatoeba()
build_tatoeba_frequency()
split_pos_lists()
build_frequency_lists()
extract_phrases()
convert_to_mochi()
# convert_to_mochi(deck_size=100)

# switch_columns(
#     SOURCES_LLM_DIR / "phrases_es_to_en.csv",
#     SOURCES_LLM_DIR / "phrases_en_to_es.csv",
# )