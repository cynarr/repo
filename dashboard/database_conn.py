import sqlite3
import pandas as pd
import datetime 
import time


def generate_where_conditions(conditions):
    where_parts = []

    if 'start_date' in conditions and 'end_date' in conditions:
        start = int(time.mktime(datetime.datetime.strptime(conditions['start_date'], "%Y-%m-%d").timetuple()))
        end = int(time.mktime(datetime.datetime.strptime(conditions['end_date'], "%Y-%m-%d").timetuple()))

        where_parts.append(f"date_publish > {start} AND date_publish < {end}")

    if len(where_parts) > 0:
        return "WHERE " + " AND ".join(where_parts)

    return ""

def get_sentiment_hist_df(conditions = {}):
    where_clause = generate_where_conditions(conditions)

    with sqlite3.connect("data/database.db", check_same_thread=False) as conn:
        query = f'SELECT date_publish FROM documents {where_clause} ORDER BY date_publish'
        df = pd.read_sql_query(query, conn)
        df = (pd.to_datetime(df['date_publish'], unit='s')
            .dt.floor('d')
            .value_counts()
            .rename_axis('date')
            .reset_index(name='Number of articles'))

        df["Sentiment"] = "Positive" 
    return df

if __name__ == "__main__":
    print(get_sentiment_hist_df({'start_date': '2020-01-01', 'end_date': '2020-05-01'}))