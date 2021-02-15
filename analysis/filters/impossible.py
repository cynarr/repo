import sys
import fileinput
import orjson


for line in sys.stdin.buffer:
    doc = orjson.loads(line)
    if doc["date_publish"] > sys.argv[1]:
        continue
    sys.stdout.buffer.write(line)
