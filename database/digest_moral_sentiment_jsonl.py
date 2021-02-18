import duckdb
import json 
import sys
from .utils import flush_rows, get_doc_id_map


SCHEMA = "moral_sentiment_scores(document_id, sentiment_type, score)"


if __name__ == '__main__':
    conn = duckdb.connect(sys.argv[1])
    doc_id_map = get_doc_id_map(conn)
    c = conn.cursor()
    conn.begin()
    counter = 0
    rows = []

    for line in sys.stdin:
        counter += 1

        doc = json.loads(line.strip())
        canon_url = doc['canon_url']
        document_id = doc_id_map.get(canon_url)
        if document_id is None:
            continue

        for sentiment_name in doc['proj_sentiment']:
            sent_score = doc['proj_sentiment'][sentiment_name]
            rows.append((document_id, sentiment_name, sent_score))

        if counter % 50000 == 0:  # Commit changes every now and then
            flush_rows(SCHEMA, conn, rows)
            conn.begin()
            print(counter)
    
    flush_rows(SCHEMA, conn, rows)
    conn.close()
