import fileinput
import orjson
from collections import Counter
from pprint import pprint


country_cnt = Counter()
lang_cnt = Counter()
date_cnt = Counter()


total = 0
for line in fileinput.input():
    doc = orjson.loads(line)
    country_cnt[doc["country"]] += 1
    lang_cnt[doc["language"]] += 1
    date_cnt[doc["date_publish"][:10]] += 1
    total += 1


def stats(name, cnt):
    print(name)
    pprint(cnt.most_common())
    pprint([(name, c / total) for name, c in cnt.most_common()])


print("Total", total)
stats("Country", country_cnt)
stats("Lang", lang_cnt)
stats("Date", date_cnt)
