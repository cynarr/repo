import sys
import orjson


for line in sys.stdin.buffer:
    doc = orjson.loads(line)
    if not doc["date_publish"].startswith(sys.argv[1]):
        continue
    sys.stdout.buffer.write(line)
