import os
from os.path import join as pjoin
from .utils.csv import read_csv_set


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
EURO_COUNTRIES = read_csv_set(pjoin(DIR_PATH, "data/euro_country.csv"))
LANGDETECT_EURO_COUNTRIES = read_csv_set(pjoin(DIR_PATH, "data/langdetect_euro_country.csv"))
EURO_LANGUAGES = read_csv_set(pjoin(DIR_PATH, "data/euro_language.csv"))


def is_european_cc(country_code: str):
    return country_code in EURO_COUNTRIES


def is_european_langcode(langcode: str):
    return langcode in EURO_LANGUAGES


def is_european_langdetect_langcode(langcode: str):
    return langcode in LANGDETECT_EURO_COUNTRIES
