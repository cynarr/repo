from ..utils.csv import read_csv_set
from ..utils.wikidata import Wikidata


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
LANGDETECT_EURO_LANGUAGES = read_csv_set(pjoin(DIR_PATH, "..", "data/langdetect_euro_language.csv"))
EURO_LANGUAGES = read_csv_set(pjoin(DIR_PATH, "..", "data/euro_language.csv"))

wikidata = Wikidata()

def make_query(ccs, langcodes):
    return """
        SELECT ?langcode ?cc2 ?lab
        WHERE
        {
          # has 2-letter country code
          ?country wdt:P297 ?cc2 .
          # is or has adminRegion (reifying neccesary to include England for some reason)
          ?country (p:P150/ps:P150)* ?adminRegion .
          # is a country (reifying neccesary to include England for some reason)
          ?adminRegion p:P31/ps:P31/wdt:P279* wd:Q6256 .
          # not a historical country
          FILTER NOT EXISTS {?adminRegion wdt:P31/wdt:P279* wd:Q3024240} .
          # cc2 in my set of values
          VALUES ?cc2 { %s } .
          # langcode in my set of values
          VALUES ?langcode { %s } .
          {
              # adminRegion has label
              ?adminRegion rdfs:label ?lab .
          } UNION {
              # or altLabel
              ?adminRegion skos:altLabel ?lab
          } .
          FILTER (lang(?lab) = ?langcode)
        }
        GROUP BY ?langcode ?cc2 ?lab
    """ % (
        " ".join(('"{}"'.format(cc2) for cc2 in ccs)),
        " ".join(('"{}"'.format(langcode) for langcode in langcodes)),
    )


results = []
for lang in LANGDETECT_EURO_LANGUAGES:
    # It's a slow query so we just go country at a time to avoid timeouts
    results.extend(
        wikidata.query_tpl(
            make_query((lang,), EURO_LANGUAGES),
            "langcode",
            "cc2",
            "lab"
        )
    )
results.sort()


print("langcode,cc2,lab")

for langcode, cc2, lab in results:
    if len(lab) <= 3:
        continue
    print(f"{langcode},{cc2},{lab}")
