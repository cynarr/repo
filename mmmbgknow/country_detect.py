import os
from os.path import join as pjoin
from .utils.csv import read_csv_map


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
FQDN_COUNTRY = read_csv_map(pjoin(DIR_PATH, "data/fqdn_country.csv"))
TLD_COUNTRY = read_csv_map(pjoin(DIR_PATH, "data/tld_country.csv"))
LANG_COUNTRY = read_csv_map(pjoin(DIR_PATH, "data/lang_country.csv"))


def get_country_known_domain(url_parts):
    return FQDN_COUNTRY.get(url_parts.registered_domain)


def get_country_from_tld(url_parts):
    suffix = "." + url_parts.suffix
    return TLD_COUNTRY.get(suffix)


def get_country_from_language(language: str):
    return LANG_COUNTRY.get(language)


def detect_country(url: str, get_lang):
    import tldextract

    url_parts = tldextract.extract(url)
    res = get_country_known_domain(url_parts)
    if res:
        return res
    res = get_country_from_tld(url_parts)
    if res:
        return res
    lang = get_lang()
    return get_country_from_language(lang)
