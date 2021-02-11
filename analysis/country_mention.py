import sys
import fileinput
import orjson
from mmmbgknow.pickled_searchers import get_country


country_searchers = get_country()
MAX_COUNTRIES = 5


for line in fileinput.input():
    doc = orjson.loads(line)
    searcher = country_searchers.get(doc["language"])
    if searcher is None:
        continue

    def match(key):
        return searcher.match((doc[key] or "").lower().encode("utf-8"))
    countries = list(match("title") | match("maintext"))
    if len(countries) > MAX_COUNTRIES:
        continue
    sys.stdout.buffer.write(orjson.dumps({
        "canon_url": doc["canon_url"],
        "country_mentions": countries,
    }) + b"\n")
