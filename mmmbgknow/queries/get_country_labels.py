from ..utils.wikidata import Wikidata
from ..european import EURO_COUNTRIES, EURO_LANGUAGES

wikidata = Wikidata()

QUERY = """
SELECT ?langcode ?cc2 ?lab
WHERE
{
  # has 2-letter country code
  ?country wdt:P297 ?cc2 .
  # cc2 in my set of values
  VALUES ?cc2 { %s } .
  # langcode in my set of values
  VALUES ?langcode { %s } .
  {
      # country has label
      ?country rdfs:label ?lab
  } UNION {
      # or altLabel
      ?country skos:altLabel ?lab
  } .
  # label in language
  FILTER (lang(?lab) = ?langcode)
}
""" % (
    " ".join(('"{}"'.format(cc2) for cc2 in EURO_COUNTRIES)),
    " ".join(('"{}"'.format(langcode) for langcode in EURO_LANGUAGES)),
)


print("QUERY", QUERY)
print("langcode,cc2,lab")

for langcode, cc2, lab in sorted(wikidata.query_tpl(QUERY, "langcode", "cc2", "lab")):
    print(f"{langcode},{cc2},{lab}")
