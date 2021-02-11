import sqlite3
import json 
import sys
import datetime
import time

# First run "cat database/database_schema.sql | sqlite3 database/database.db" to create the scehma on command line

if __name__ == '__main__':
    conn = sqlite3.connect("database/database.db")
    c = conn.cursor()
    counter = 0

    for line in sys.stdin:
        counter += 1

        doc = json.loads(line.strip())
        
        canon_url = doc['canon_url']
        date_publish = doc['date_publish']
        language = doc['language']
        title = doc['title']
        country = doc['country']

        # Tranform date into unix time as SQLite does not handle dates
        dt = datetime.datetime.strptime(date_publish, '%Y-%m-%dT%H:%M:%S')
        date_publish_unix = int(time.mktime(dt.timetuple()))

        try:
            c.execute("INSERT INTO documents(canon_url, date_publish, language, title, country) VALUES (?, ?, ?, ?, ?)", (canon_url, date_publish_unix, language, title, country))
        except sqlite3.IntegrityError as err:
            print("Warning:", err)
        except sqlite3.OperationalError as err:
            print("Error:", err)
            exit()

        if counter % 100: # Commit changes every now and then
            conn.commit()            

    conn.commit()
    conn.close()