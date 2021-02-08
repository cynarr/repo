import tldextract

from ..utils.wikidata import Wikidata

wikidata = Wikidata()

QUERY = """
SELECT ?website ?cc
WHERE
{
  ?item wdt:P31 ?class.
  ?class wdt:P279* wd:Q1193236.
  ?item wdt:P856 ?website .
  ?item wdt:P159 ?hqLoc .
  ?hqLoc wdt:P17 ?country .
  ?country wdt:P30 wd:Q46 .
  ?country wdt:P297 ?cc
}
"""


print("domain,cc2")
for row in wikidata.query(QUERY):
    url = row["website"]["value"]
    url_parts = tldextract.extract(url)
    domain = url_parts.registered_domain
    is_cctld = len(url_parts.suffix.rsplit(".", 1)[-1]) == 2
    if is_cctld:
        continue
    cc2 = row["cc"]["value"]
    print(f"{domain},{cc2}")
