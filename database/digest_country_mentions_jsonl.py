import sqlite3
import orjson
import sys


if __name__ == '__main__':
    conn = sqlite3.connect(sys.argv[1])
    c = conn.cursor()
    counter = 0

    for line in sys.stdin.buffer:
        counter += 1

        doc = orjson.loads(line)
        canon_url = doc['canon_url']

        if not doc['country_mentions']:
            continue

        doc_id = c.execute("SELECT document_id FROM documents WHERE canon_url = ?", (canon_url,)).fetchone()[0]
        for country in doc['country_mentions']:
            c.execute("INSERT INTO country_mentions(document_id, mention_country) VALUES (?, ?)", (doc_id, country))

        if counter % 5000 == 0:  # Commit changes every now and then
            conn.commit()

    conn.commit()
    conn.close()
