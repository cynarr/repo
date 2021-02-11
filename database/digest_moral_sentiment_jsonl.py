import sqlite3
import json 
import sys

# First run "cat database/database_schema.sql | sqlite3 database/database.db" to create the scehma on command line

if __name__ == '__main__':
    conn = sqlite3.connect("database/database.db")
    c = conn.cursor()

    for line in sys.stdin:
        doc = json.loads(line.strip())
        canon_url = doc['canon_url']

        for sentiment_name in doc['proj_sentiment']:
            sent_score = doc['proj_sentiment'][sentiment_name]
            try:
                c.execute(f"INSERT INTO moral_sentiment_scores(canon_url, sentiment_type, score) VALUES (?, ?, ?)", (canon_url, sentiment_name, sent_score))
            except sqlite3.IntegrityError:
                print(f"Duplicate entry for '{canon_url}'")
    
    conn.commit()
    conn.close()