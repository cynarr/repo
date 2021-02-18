import duckdb
import json 
import sys

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

        if counter % 5000 == 0:  # Commit changes every now and then
            conn.commit()
            c.executemany(f"INSERT INTO moral_sentiment_scores(document_id, sentiment_type, score) VALUES (?, ?, ?)", rows)
            rows = []
            conn.begin()
    
    conn.commit()
    conn.close()
