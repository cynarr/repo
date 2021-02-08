from ..utils.wikidata import Wikidata

wikidata = Wikidata()

QUERY = """
SELECT ?cc2 ?langcode2
WHERE
{
  ?country wdt:P297 ?cc2 .
  ?country wdt:P37 ?lang .
  ?lang wdt:P218 ?langcode2
}
"""


print("cc2,langcode2")
result = {}
for row in wikidata.query(QUERY):
    result.setdefault(row["langcode2"]["value"], []).append(row["cc2"]["value"])


for langcode, cc2 in result.items():
    if len(cc2) > 1:
        continue
    print(f"{langcode},{cc2[0]}")
