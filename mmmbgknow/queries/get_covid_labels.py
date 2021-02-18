import os
from os.path import join as pjoin
from ..utils.csv import read_csv_set
from ..utils.wikidata import Wikidata


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
EURO_COUNTRIES = read_csv_set(pjoin(DIR_PATH, "..", "data/euro_country.csv"))
EURO_LANGUAGES = read_csv_set(pjoin(DIR_PATH, "..", "data/euro_language.csv"))

wikidata = Wikidata()

COVID_ENTITIES = ["Q84263196", "Q82069695", "Q89469904"]

QUERY = """
SELECT ?langcode ?lab
WHERE
{
  # covid in my set of values
  VALUES ?covid { %s } .
  # langcode in my set of values
  VALUES ?langcode { %s } .
  {
      # covid has label
      ?covid rdfs:label ?lab
  } UNION {
      # or altLabel
      ?covid skos:altLabel ?lab
  } .
  # label in language
  FILTER (lang(?lab) = ?langcode)
}
""" % (
    " ".join(('wd:{}'.format(covid) for covid in COVID_ENTITIES)),
    " ".join(('"{}"'.format(langcode) for langcode in EURO_LANGUAGES)),
)


print("langcode,lab")
for langcode, lab in sorted(wikidata.query_tpl(QUERY, "langcode", "lab")):
    print(f"{langcode},{lab}")
