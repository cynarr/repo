import sqlite3
import pandas as pd

def get_datehist_df(start_date=-1, end_date=-1):
    conn = sqlite3.connect("data/database.db", check_same_thread=False)
    query = 'SELECT date_publish FROM documents'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

if __name__ == "__main__":
    print(get_datehist_df())