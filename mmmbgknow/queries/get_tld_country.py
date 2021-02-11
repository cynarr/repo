from ..utils.wikidata import Wikidata

wikidata = Wikidata()

QUERY = """
SELECT (SAMPLE(?cc2) AS ?cc2u) (SAMPLE(?tldLab) AS ?tldLabu)
WHERE
{
  # is a country
  ?country wdt:P31/wdt:P279* wd:Q6256 .
  # not a historical country
  FILTER NOT EXISTS {?country wdt:P31/wdt:P279* wd:Q3024240}
  # has 2-letter country code
  ?country wdt:P297 ?cc2 .
  # has tld including a tld only for part of the country
  ?country p:P78 ?countryTldStatement .
  ?countryTldStatement ps:P78 ?tld .
  OPTIONAL {?countryTldStatement pq:P518 ?part} .
  # has English language label
  ?tld rdfs:label ?tldLab .
  FILTER (langMatches( lang(?tldLab), "EN" ) )
}
# The country code is unique for a given tld
GROUP BY ?cc2 ?tld
HAVING(COUNT(DISTINCT ?cc2) = 1)
"""


print("tld,cc2")
for tld, cc2 in sorted(wikidata.query_tpl(QUERY, "tldLabu", "cc2u")):
    print(f"{tld},{cc2}")
