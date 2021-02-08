from SPARQLWrapper import SPARQLWrapper, JSON, __agent__ as __sparqlwrapper_agent__
import tldextract

__agent__ = (
    "Mood Mapping Muppet's Covid Mood Map/0.0 " +
    "(https://github.com/mood-mapping-muppets/repo/) " +
    __sparqlwrapper_agent__
)

sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent=__agent__)

sparql.setQuery("""
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
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()


print("domain,cc2")
for row in results['results']['bindings']:
    url = row["website"]["value"]
    url_parts = tldextract.extract(url)
    domain = url_parts.registered_domain
    is_cctld = len(url_parts.suffix.rsplit(".", 1)[-1]) == 2
    if is_cctld:
        continue
    cc2 = row["cc"]["value"]
    print(f"{domain},{cc2}")
