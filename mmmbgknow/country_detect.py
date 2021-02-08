import os
from os.path import join as pjoin


dir_path = os.path.dirname(os.path.realpath(__file__))


def read_csv_map(filename):
    import csv

    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        return {rows[0]: rows[1] for rows in reader}


FQDN_COUNTRY = read_csv_map(pjoin(dir_path, "data/fqdn_country.csv"))
TLD_COUNTRY = read_csv_map(pjoin(dir_path, "data/tld_country.csv"))
LANG_COUNTRY = read_csv_map(pjoin(dir_path, "data/lang_country.csv"))


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


def is_european(country_code: str):
    from pycountry_convert import country_alpha2_to_continent_code

    return country_alpha2_to_continent_code(country_code) == "EU"
