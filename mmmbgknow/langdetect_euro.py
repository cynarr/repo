import os
from os.path import join as pjoin
from .utils.csv import read_csv_set

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
EURO_LANGUAGES = read_csv_set(pjoin(DIR_PATH, "data/euro_language.csv"))
LANGDETECT_LANGUAGES = read_csv_set(pjoin(DIR_PATH, "data/langdetect_languages.csv"))


print("cc2")
for lang in sorted(EURO_LANGUAGES & LANGDETECT_LANGUAGES):
    print(lang)
