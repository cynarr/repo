from ..utils.wikidata import Wikidata

wikidata = Wikidata()

QUERY = """
SELECT (SAMPLE(?langcode2) AS ?langcode2u)
WHERE
{
  # is a country
  ?country wdt:P31/wdt:P279* wd:Q6256 .
  # not a historical country
  FILTER NOT EXISTS {?country wdt:P31/wdt:P279* wd:Q3024240}
  # has continent: Europe
  ?country wdt:P30 wd:Q46 .
  # has official language, possibly only official in a part of it
  ?country p:P37 ?countryLangStatement .
  ?countryLangStatement ps:P37 ?lang .
  OPTIONAL {?countryLangStatement pq:P518 ?part} .
  # has 2-letter language code
  ?lang wdt:P218 ?langcode2
}
GROUP BY ?langcode2
"""


print("langcode2")
for langcode2, in sorted(wikidata.query_tpl(QUERY, "langcode2u")):
    print(langcode2)
