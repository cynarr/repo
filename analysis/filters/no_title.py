import sys
import orjson


for line in sys.stdin.buffer:
    doc = orjson.loads(line)
    if not doc["title"]:
        continue
    sys.stdout.buffer.write(line)
