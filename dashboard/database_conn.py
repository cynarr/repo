import sqlite3
import pandas as pd
import datetime 
import time


def generate_where_conditions(conditions): # TODO: switch conditions dict to kwargs
    where_parts = []

    if 'start_date' in conditions and 'end_date' in conditions:
        start = int(time.mktime(datetime.datetime.strptime(conditions['start_date'], "%Y-%m-%d").timetuple()))
        end = int(time.mktime(datetime.datetime.strptime(conditions['end_date'], "%Y-%m-%d").timetuple()))

        where_parts.append(f"d.date_publish > {start} AND d.date_publish < {end}")

    if 'language' in conditions and len(conditions['language']) > 0:
        where_parts.append(f"d.language = '{conditions['language']}'")

    if len(where_parts) > 0:
        return "WHERE " + " AND ".join(where_parts)

    return ""

def get_sentiment_hist_df(conditions = {}):
    where_clause = generate_where_conditions(conditions)

    with sqlite3.connect("database/database.db", check_same_thread=False) as conn:
        query = f'SELECT date_publish FROM documents AS d {where_clause} ORDER BY d.date_publish'
        df = pd.read_sql_query(query, conn)
        df = (pd.to_datetime(df['date_publish'], unit='s')
            .dt.floor('d')
            .value_counts()
            .rename_axis('date')
            .reset_index(name='Number of articles'))

        df["Sentiment"] = "Positive" 
    return df

def get_moral_sentiment_hist_df(conditions = {}):
    where_clause = generate_where_conditions(conditions)

    with sqlite3.connect("database/database.db", check_same_thread=False) as conn:
        query = " ".join([
            f"SELECT date_publish, sentiment_type, score FROM documents AS d JOIN moral_sentiment_scores AS m ON d.canon_url = m.canon_url",
            where_clause,
            "ORDER BY d.date_publish"
        ])
        df = pd.read_sql_query(query, conn)
        df['date'] = pd.to_datetime(df['date_publish'], unit='s').dt.floor('d')

    return (df.groupby(['date', 'sentiment_type'])['score']
        .agg(['sum','count'])
        .reset_index())

if __name__ == "__main__":
    print(get_moral_sentiment_hist_df({'start_date': "2020-03-01", 'end_date': "2020-03-02"}))