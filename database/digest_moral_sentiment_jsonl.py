import duckdb
import json 
import sys
from .utils import flush_rows


SCHEMA = "moral_sentiment_scores(document_id, sentiment_type, score)"


if __name__ == '__main__':
    conn = duckdb.connect(sys.argv[1])
    c = conn.cursor()
    conn.begin()
    counter = 0
    rows = []

    for line in sys.stdin:
        counter += 1

        doc = json.loads(line.strip())
        canon_url = doc['canon_url']
        doc_id = c.execute("SELECT document_id FROM documents WHERE canon_url = ?", (canon_url,)).fetchone()[0]

        for sentiment_name in doc['proj_sentiment']:
            sent_score = doc['proj_sentiment'][sentiment_name]
            rows.append((doc_id, sentiment_name, sent_score))

        if counter % 50000 == 0:  # Commit changes every now and then
            flush_rows(SCHEMA, conn, rows)
            conn.begin()
            print(counter)
    
    flush_rows(SCHEMA, conn, rows)
    conn.close()
