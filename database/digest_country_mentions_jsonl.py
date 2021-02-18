import duckdb
import orjson
import sys
from .utils import flush_rows


SCHEMA = "country_mentions(document_id, mention_country)"


if __name__ == '__main__':
    conn = duckdb.connect(sys.argv[1])
    c = conn.cursor()
    conn.begin()
    counter = 0
    rows = []

    for line in sys.stdin.buffer:
        counter += 1

        doc = orjson.loads(line)
        canon_url = doc['canon_url']

        if not doc['country_mentions']:
            continue

        doc_id = c.execute("SELECT document_id FROM documents WHERE canon_url = ?", (canon_url,)).fetchone()[0]
        for country in doc['country_mentions']:
            rows.append((doc_id, country))

        if counter % 50000 == 0:  # Commit changes every now and then
            flush_rows(SCHEMA, conn, rows)
            conn.begin()
            print(counter)

    flush_rows(SCHEMA, conn, rows)
    conn.close()
