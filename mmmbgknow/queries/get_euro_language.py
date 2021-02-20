import os
from os.path import join as pjoin

from ..utils.wikidata import Wikidata
from ..utils.csv import read_csv_set

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
EURO_COUNTRIES = read_csv_set(pjoin(DIR_PATH, "..", "data/euro_country.csv"))

wikidata = Wikidata()

QUERY = """
SELECT (SAMPLE(?langcode2) AS ?langcode2u)
WHERE
{
  # has 2-letter country code
  ?country wdt:P297 ?cc .
  # has official language, possibly only official in a part of it
  ?country p:P37 ?countryLangStatement .
  ?countryLangStatement ps:P37 ?lang .
  OPTIONAL {?countryLangStatement pq:P518 ?part} .
  # has 2-letter language code
  ?lang wdt:P218 ?langcode2
  # cc in my set of values
  VALUES ?cc { %s }
}
GROUP BY ?langcode2
""" % (
    " ".join(('"{}"'.format(cc2) for cc2 in EURO_COUNTRIES)),
)


print("langcode2")
for langcode2, in sorted(wikidata.query_tpl(QUERY, "langcode2u")):
    print(langcode2)
