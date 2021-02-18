import duckdb
import sqlite3
import json 
import sys
import datetime
import time

# First run "cat database/database_schema.sql | sqlite3 database/database.db" to create the scehma on command line


if __name__ == '__main__':
    conn = duckdb.connect(sys.argv[1])
    cursor = conn.cursor()
    conn.begin()
    counter = 0
    rows = []

    for line in sys.stdin:
        counter += 1

        doc = json.loads(line.strip())
        
        canon_url = doc['canon_url']
        date_publish = doc['date_publish']
        language = doc['language']
        title = doc['title']
        country = doc['country']

        rows.append((canon_url, date_publish, language, title, country))

        if counter % 50000 == 0:  # Commit changes every now and then
            cursor.executemany("INSERT INTO documents(document_id, canon_url, date_publish, language, title, country) VALUES (nextval('document_id_seq'), ?, ?, ?, ?, ?)", rows)
            conn.commit()
            rows = []
            conn.begin()
            print(counter)

    conn.commit()
    conn.close()
