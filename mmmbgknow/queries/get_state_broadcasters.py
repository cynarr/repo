import tldextract

from ..european import EURO_COUNTRIES
from ..utils.wikidata import Wikidata

MANUAL_ENTRIES = [
    ("LI", "radio.li"),
    ("KZ", "kaztrk.kz"),
]

wikidata = Wikidata()

QUERY_EASY_WAY = """
# is public broadcaster
{ ?item wdt:P31/wdt:P279* wd:Q1126006 }
UNION
# or member of European Broadcasting union
{ ?item wdt:P463 wd:Q166400 }
"""

QUERY_HARD_WAY = """
{
  # is organisation
  ?item wdt:P31/wdt:P279* wd:Q43229 .
  # is a state-owned enterprise
  ?item wdt:P1454/wdt:P279* wd:Q270791
}
UNION
{
  # is organisation
  ?item wdt:P31/wdt:P279* wd:Q43229 .
  # is owned by a government
  ?item wdt:P127/wdt:P31 wd:Q7188
}
# is a statutory organsation
UNION
{
   ?item wdt:P31/wdt:P279* wd:Q699386
} .
{
  # in the journalism industry
  ?item wdt:P452/wdt:P279* wd:Q11030 .
}
UNION
{
  # in the mass media industry
  ?item wdt:P452/wdt:P279* wd:Q11033 .
}
UNION
{
  # is a broadcaster
  ?item wdt:P31/wdt:P279* wd:Q15265344 .
}
"""


def make_query(ccs, public_broadcaster_subquery):
    return """
    SELECT ?website ?cc
    WHERE
    {
      %s .
      # it or a subsidary has an official website
      ?item wdt:P355*/wdt:P856 ?website .
      # has a country
      ?item wdt:P17 ?country .
      # has 2-letter country code
      ?country wdt:P297 ?cc .
      # cc in my set of values
      VALUES ?cc { %s }
    }
    """ % (
        public_broadcaster_subquery,
        " ".join(('"{}"'.format(cc2) for cc2 in ccs)),
    )


countries = set()
result = {}
for country in EURO_COUNTRIES:
    for subquery in [QUERY_EASY_WAY, QUERY_HARD_WAY]:
        got_something = False
        query = make_query((country,), subquery)
        query_result = wikidata.query_tpl(query, "website", "cc")
        for url, cc2 in query_result:
            got_something = True
            url_parts = tldextract.extract(url)
            domain = url_parts.registered_domain
            result.setdefault(domain, set()).add(cc2)
            countries.add(cc2)
        if got_something:
            break

for cc2, domain in MANUAL_ENTRIES:
    result.setdefault(domain, set()).add(cc2)
    countries.add(cc2)


assert countries == EURO_COUNTRIES, f"missing: {EURO_COUNTRIES - countries}"


print("domain,cc2")
for domain, cc2_set in sorted(result.items()):
    if len(cc2_set) > 1:
        continue
    cc2 = next(iter(cc2_set))
    print(f"{domain},{cc2}")
