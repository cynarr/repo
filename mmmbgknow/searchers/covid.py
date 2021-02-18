import os
from os.path import join as pjoin
import sys
import pickle

from ..utils.csv import read_csv_map_set
from ..european import LANGDETECT_EURO_LANGUAGES
from ..search import MatchSearcher


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
COVID_LABELS = read_csv_map_set(pjoin(DIR_PATH, "..", "data/covid_labels.csv"))
COVID_LABELS["no"] = COVID_LABELS["nb"] | COVID_LABELS["nn"]

# Make sure we always have the basic informal patterns
EXTRA_PATTERNS = [
    br"corona\pL*",
    br"korona\pL*",
    br"covid\pL*",
    r"корона\pL*".encode("utf-8")
]


searchers = {}
for lang in LANGDETECT_EURO_LANGUAGES:
    assert lang in COVID_LABELS, f"'{lang}' not in {COVID_LABELS.keys()}"
    all_labels = COVID_LABELS[lang]
    if lang != "en":
        all_labels |= COVID_LABELS["en"]
    searchers[lang] = MatchSearcher(all_labels, extra_patterns=EXTRA_PATTERNS)


with open(sys.argv[1], "wb") as outf:
    pickle.dump(searchers, outf)
