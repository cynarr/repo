import duckdb
import orjson
import sys
from .utils import flush_rows, get_doc_id_map


SCHEMA = "mbert_sentiment(document_id, sentiment)"


if __name__ == '__main__':
    conn = duckdb.connect(sys.argv[1])
    doc_id_map = get_doc_id_map(conn)
    c = conn.cursor()
    conn.begin()
    counter = 0
    rows = []

    for line in sys.stdin.buffer:
        counter += 1

        doc = orjson.loads(line)
        canon_url = doc['canon_url']
        document_id = doc_id_map.get(canon_url)
        if document_id is None:
            continue

        rows.append((document_id, doc['sentiment']))

        if counter % 50000 == 0:  # Commit changes every now and then
            flush_rows(SCHEMA, conn, rows)
            conn.begin()
            print(counter)

    flush_rows(SCHEMA, conn, rows)
    conn.close()
