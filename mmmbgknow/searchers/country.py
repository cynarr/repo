import os
from os.path import join as pjoin
import pickle
import sys

from ..utils.csv import read_csv_map_map_set
from ..european import LANGDETECT_EURO_COUNTRIES
from ..search import MapSearcher


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
COUNTRY_LABELS = (
    read_csv_map_map_set(pjoin(DIR_PATH, "..", "data/country_labels.csv"))
)
COUNTRY_LABELS["no"] = {**COUNTRY_LABELS["nb"], **COUNTRY_LABELS["nn"]}


searchers = {}
for lang in LANGDETECT_EURO_COUNTRIES:
    assert lang in COUNTRY_LABELS, f"'{lang}' not in {COUNTRY_LABELS.keys()}"
    all_country_labels = COUNTRY_LABELS[lang]
    searchers[lang] = MapSearcher(all_country_labels)


with open(sys.argv[1], "wb") as outf:
    pickle.dump(searchers, outf)
