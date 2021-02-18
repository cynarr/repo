import duckdb
import orjson
import sys


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
            conn.commit()
            c.executemany("INSERT INTO country_mentions(document_id, mention_country) VALUES (?, ?)", rows)
            rows = []
            conn.begin()
            print(counter)

    conn.commit()
    conn.close()
