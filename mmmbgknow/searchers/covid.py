import os
from os.path import join as pjoin
import sys
import pickle

from ..utils.csv import read_csv_map_set
from ..european import EURO_LANGUAGES
from ..search import MatchSearcher


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
COVID_LABELS = read_csv_map_set(pjoin(DIR_PATH, "..", "data/covid_labels.csv"))


searchers = {}
for lang in EURO_LANGUAGES:
    all_labels = COVID_LABELS.get(lang, set())
    if lang != "en":
        all_labels |= COVID_LABELS["en"]
    searchers[lang] = MatchSearcher(all_labels)


with open(sys.argv[1], "wb") as outf:
    pickle.dump(searchers, outf)
