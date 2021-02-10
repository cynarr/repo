import os
from os.path import join as pjoin
import pickle


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
COVID_SEARCH = pjoin(DIR_PATH, "data/covid_search.pkl")
COUNTRY_SEARCH = pjoin(DIR_PATH, "data/country_search.pkl")


def get_covid():
    with open(COVID_SEARCH, "rb") as inf:
        return pickle.load(inf)


def get_country():
    with open(COUNTRY_SEARCH, "rb") as inf:
        return pickle.load(inf)
