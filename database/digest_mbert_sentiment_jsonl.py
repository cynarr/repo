import duckdb
import orjson
import sys


SCHEMA = "mbert_sentiment(document_id, sentiment)"


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

        doc_id = c.execute("SELECT document_id FROM documents WHERE canon_url = ?", (canon_url,)).fetchone()[0]
        rows.append((doc_id, doc['sentiment']))

        if counter % 50000 == 0:  # Commit changes every now and then
            flush_rows(SCHEMA, conn, rows)
            conn.begin()
            print(counter)

    flush_rows(SCHEMA, conn, rows)
    conn.close()
