from ..utils.wikidata import Wikidata

wikidata = Wikidata()

QUERY = """
SELECT ?cc2 ?langcode2
WHERE
{

  # has 2-letter country code
  ?country wdt:P297 ?cc2 .
  # has language
  ?country wdt:P37 ?lang .
  # has 2-letter language code
  ?lang wdt:P218 ?langcode2
}
"""


print("langcode2,cc2")
result = {}
for langcode2, cc2 in wikidata.query_tpl(QUERY, "langcode2", "cc2"):
    result.setdefault(langcode2, set()).add(cc2)


for langcode, cc2_set in sorted(result.items()):
    if len(cc2_set) > 1:
        continue
    cc2 = next(iter(cc2_set))
    print(f"{langcode},{cc2}")
