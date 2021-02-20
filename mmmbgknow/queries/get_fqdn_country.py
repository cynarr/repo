import os
from os.path import join as pjoin
import tldextract

from ..utils.csv import read_csv_set
from ..utils.wikidata import Wikidata


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
EURO_COUNTRIES = read_csv_set(pjoin(DIR_PATH, "..", "data/euro_country.csv"))

wikidata = Wikidata()

QUERY = """
SELECT ?website ?cc
WHERE
{
  # is news media
  ?item wdt:P31/wdt:P279* wd:Q1193236 .
  # not news agency (tend to be international + deliberately neutral)
  FILTER NOT EXISTS {?item wdt:P31/wdt:P279* wd:Q192283}
  # has an official website
  ?item wdt:P856 ?website .
  # has a headquarters
  ?item wdt:P159 ?hqLoc .
  # headquaters has a country
  ?hqLoc wdt:P17 ?country .
  # has 2-letter country code
  ?country wdt:P297 ?cc
  # cc in my set of values
  VALUES ?cc { %s }
}
""" % (
    " ".join(('"{}"'.format(cc2) for cc2 in EURO_COUNTRIES)),
)


result = {}
for url, cc2 in wikidata.query_tpl(QUERY, "website", "cc"):
    url_parts = tldextract.extract(url)
    domain = url_parts.registered_domain
    is_cctld = len(url_parts.suffix.rsplit(".", 1)[-1]) == 2
    if is_cctld:
        continue
    result.setdefault(domain, set()).add(cc2)


print("domain,cc2")
for domain, cc2_set in sorted(result.items()):
    if len(cc2_set) > 1:
        continue
    cc2 = next(iter(cc2_set))
    print(f"{domain},{cc2}")
