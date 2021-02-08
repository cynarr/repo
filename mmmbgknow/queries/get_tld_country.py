from ..utils.wikidata import Wikidata

wikidata = Wikidata()

QUERY = """
SELECT (SAMPLE(?cc2) AS ?cc2u) (SAMPLE(?tldLab) AS ?tldLabu)
WHERE
{
  ?country wdt:P31 wd:Q6256 .
  ?country wdt:P297 ?cc2 .
  ?country p:P78 ?countryTldStatement .
  ?countryTldStatement ps:P78 ?tld .
  OPTIONAL {?countryTldStatement pq:P518 ?part} .
  ?tld rdfs:label ?tldLab .
  FILTER (langMatches( lang(?tldLab), "EN" ) )
}
GROUP BY ?cc2 ?tld
HAVING(COUNT(DISTINCT ?cc2) = 1)
"""


print("cc2,tld")
for row in wikidata.query(QUERY):
    cc2 = row["cc2u"]["value"]
    tld = row["tldLabu"]["value"]
    print(f"{tld},{cc2}")
