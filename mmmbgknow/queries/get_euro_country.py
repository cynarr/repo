from ..utils.wikidata import Wikidata

wikidata = Wikidata()

QUERY = """
SELECT ?cc2
WHERE
{
  # is a country
  ?country wdt:P31/wdt:P279* wd:Q6256 .
  # not a historical country
  FILTER NOT EXISTS {?country wdt:P31/wdt:P279* wd:Q3024240}
  # has continent: Europe
  ?country wdt:P30 wd:Q46 .
  # has 2-letter country code
  ?country wdt:P297 ?cc2 .
}
"""


print("cc2")
for cc2, in sorted(wikidata.query_tpl(QUERY, "cc2")):
    print(cc2)
