import os
from os.path import join as pjoin
from .utils.csv import read_csv_map_map_set


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
COUNTRY_LABELS = read_csv_map_map_set(pjoin(DIR_PATH, "data/country_labels.csv"))
EN_COUNTRY_LABELS = COUNTRY_LABELS["en"]
