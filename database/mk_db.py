import sys
import duckdb

conn = duckdb.connect(sys.argv[2])
c = conn.cursor()
c.execute(open(sys.argv[1]).read())
conn.commit()
conn.close()
