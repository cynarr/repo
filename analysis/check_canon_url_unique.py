from collections import Counter
import sys
import orjson


cnt = Counter()


for line in sys.stdin.buffer:
    doc = orjson.loads(line)
    cnt[doc["canon_url"]] += 1


for curl, num in cnt.most_common():
    if num <= 1:
        continue
    print(num, curl)
