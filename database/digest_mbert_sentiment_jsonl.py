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

        doc_id = c.execute("SELECT document_id FROM documents WHERE canon_url = ?", (canon_url,)).fetchone()[0]
        c.execute("INSERT INTO mbert_sentiment(document_id, sentiment) VALUES (?, ?)", (doc_id, doc['sentiment']))

        if counter % 5000 == 0:  # Commit changes every now and then
            conn.commit()

    conn.commit()
    conn.close()
